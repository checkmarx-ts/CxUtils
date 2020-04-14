
# Default CxFlow properties
Param(
    # CxFlow parameters
    [Parameter(
        Mandatory = $false,
        HelpMessage = "CxFlow Jar File Path"
    )][string[]] $CXFLOW_JAR = "cx-flow.jar",
    [Parameter(
        Mandatory = $false,
        HelpMessage = "CxFlow Configuration location"
    )][string[]] $CXFLOW_CONFIG = "application.yml",
    [Parameter(
        Mandatory = $false,
        HelpMessage = "CxFlow Mode"
    )][string[]] $CXFLOW_MODE = "scan",
    [Parameter(
        Mandatory = $false,
        HelpMessage = "CxFlow Break Build (true/false)"
    )][string[]] $CXFLOW_BREAK = "false",
    [Parameter(
        Mandatory = $false,
        HelpMessage = "CxFlow Scan Path"
    )][string[]] $CXFLOW_PATH = $(Get-Location).Path,
    # Checkmarx based variables
    [Parameter(
        Mandatory = $false,
        HelpMessage = "Checkmarx URI/URL"
    )][string[]] $CHECKMARX_URI = $env:CHECKMARX_URI,
    [Parameter(
        Mandatory = $false,
        HelpMessage = "Checkmarx Username"
    )][string[]] $CHECKMARX_USER = $env:CHECKMARX_USER,
    [Parameter(
        Mandatory = $false,
        HelpMessage = "Checkmarx Password"
    )][string[]] $CHECKMARX_PASSWORD = $env:CHECKMARX_PASSWORD,
    [Parameter(
        Mandatory = $false,
        HelpMessage = "Checkmarx Project"
    )][string[]] $CHECKMARX_PROJECT = $env:CHECKMARX_PROJECT,
    [Parameter(
        Mandatory = $false,
        HelpMessage = "Location of the Checkmarx XML report"
    )][string[]] $CHECKMARX_XML_PATH = "Checkmarx\Reports\ScanReport.xml",
    # Azure
    [Parameter(
        Mandatory = $false,
        HelpMessage = "Location of the Checkmarx XML report"
    )][string[]] $AZURE_URL = $env:SYSTEM_TEAMFOUNDATIONCOLLECTIONURI,
    [Parameter(
        Mandatory = $false,
        HelpMessage = "Azure Project name"
    )][string[]] $AZURE_PROJECT = $env:BUILD_REPOSITORY_NAME,
    [Parameter(
        Mandatory = $false,
        HelpMessage = "Azure Branch name"
    )][string[]] $AZURE_BRANCH = "$env:BUILD_SOURCEBRANCHNAME",
    [Parameter(
        Mandatory = $false,
        HelpMessage = "Azure Team name"
    )][string[]] $AZURE_TEAM = "$env:SYSTEM_TEAMPROJECT",
    [Parameter(
        Mandatory = $false,
        HelpMessage = "Azure Bug Issue Type in Boards"
    )][string[]] $AZURE_BUGTYPE = "issue",

    # Other
    [Parameter(
        Mandatory = $false,
        HelpMessage = "CxFlow auto-downloader (true/false)"
    )][switch] $CXFLOW_AUTODOWNLOADER
)

Write-Host "   _____             ______ _"
Write-Host "  / ____|           |  ____| |                      /\"
Write-Host " | |    __  ________| |__  | | _____      ________ /  \    _____   _ _ __ ___ "
Write-Host " | |    \ \/ /______|  __| | |/ _ \ \ /\ / /______/ /\ \  |_  / | | | '__/ _ \"
Write-Host " | |____ >  <       | |    | | (_) \ V  V /      / ____ \  / /| |_| | | |  __/"
Write-Host "  \_____/_/\_\      |_|    |_|\___/ \_/\_/      /_/    \_\/___|\__,_|_|  \___|"
Write-Host "                                                                              "
Write-Host ""


if ($DebugPreference -eq "Continue") {
    # Add better debug support for Springboot
    $env:DEBUG = "1"
}
elseif ($env:DEBUG -eq "1") {
    # if the default DEBUG variable is set, turn on the Powershell debugging
    $DebugPreference = "Continue"
}


# Auto-Downloader
if (-not (Test-Path $CXFLOW_JAR)) {
    Write-Warning "CxFlow Jar is not found on system..."

    # Check is auto-downloading is allow in current enviroment
    if (!$CXFLOW_AUTODOWNLOADER) {
        Write-Error "CxFlow's auto-downloader is disabled (use -CxFlow_AutoDownloader flag)"
        exit 1
    }

    # Run the Invoke-RestMethod/WebRequest is silent mode
    $progressPreference = 'silentlyContinue'

    # Using the GitHub API to get latest release
    try {
        $Response = Invoke-RestMethod "https://api.github.com/repos/checkmarx-ts/cx-flow/releases/latest" `
            -ErrorVariable RestError -ErrorAction SilentlyContinue
    } catch {
        Write-Error "Failed to call the GitHub API to get latest version of CxFlow..."
        exit 1
    }

    $asset = $response.assets[0]
    # Make sure its a java JAR archive before downloading
    if ($asset.content_type -eq "application/java-archive") {
        Write-Debug "CxFlow asset is a Jar"

        $Version = $Response.name
        $assetUri = $asset.browser_download_url
        $assetCreated = $asset.created_at
        # Log some variables to show version and endpoint that is being called
        Write-Host "CxFlow Download - Version :: $Version"
        Write-Host "CxFlow Download - Creation date :: $assetCreated"
        Write-Host "CxFlow Download - URI endpoint :: $assetUri"

        try {
            # Downlaod the latest JAR file
            Write-Host "Downloading Jar..."
            Invoke-WebRequest -Uri $assetUri -OutFile "$CXFLOW_JAR"
        }
        catch {
            Write-Error "Failed to download JAR file from Github..."
            exit 1
        }
        Write-Host "CxFlow Download - Completed"
    }

}
else {
    Write-Debug "CxFlow Jar is found on system..."
}

if ([System.IO.File]::Exists($CHECKMARX_XML_PATH)) {
    # If the XML report file exists, the plugin or CLI have executed
    # before CxFlow. In this case, we want to run CxFlow in Parsing
    # mode and pick up the file to create tickets.
    Write-Debug "Running in 'parse' mode"

    $CXFLOW_MODE = "parse"
    $CXFLOW_PATH = "$CHECKMARX_XML_PATH"
}

if (!$CHECKMARX_PROJECT) {
    # If the Project name isn't passed in, use the Git Repo project
    Write-Debug "Using name from pipeline as CHECKMARX_PROJECT is not set"
    $CHECKMARX_PROJECT = $env:BUILD_REPOSITORY_NAME
}

If ($CXFLOW_MODE -eq "scan") {
    # Test if there are any files/folders being passed into the eviroment (including Docker).
    # If "0" is returned, not files are present.
    Write-Debug "Scan mode is enabled"
    Write-Debug "Checking - files/folders in working directory"
    if (( Get-ChildItem "$CXFLOW_PATH" | Measure-Object ).Count -eq 0) {
        Write-Error "No files/folders in working directory..."
        exit 1
    }
}

# Encryption Algorithm
if (($env:CXFLOW_KEY)) {
    Write-Debug "Jasypt is being used to decrypt sensitive information"

    $env:JASYPT_ENCRYPTOR_PASSWORD = "$env:CXFLOW_KEY"
    if (-not (Test-Path $env:CXFLOW_KEY_ALGORITHM)) {
        # Default algorithm
        $env:JASYPT_ENCRYPTOR_ALGORITHM = "PBEWITHHMACSHA512ANDAES_256"
    }
    else {
        $env:JASYPT_ENCRYPTOR_ALGORITHM = $env:CXFLOW_KEY_ALGORITHM
    }
} else {
    Write-Debug "Not using Jasypt to decrypt tokens..."
}



# CxFlow properties
Write-Debug "CxFlow Jar :: $CXFLOW_JAR"
Write-Debug "CxFlow Config :: $CXFLOW_CONFIG"
Write-Host "CxFlow Mode :: $CXFLOW_MODE"
Write-Host "CxFlow Break :: $CXFLOW_BREAK"
Write-Debug "CxFlow AutoDownloader :: $CXFLOW_AUTODOWNLOADER"
Write-Debug "CxFlow WorkingDir :: $CXFLOW_PATH"
Write-Debug "CxFlow KeyAlg :: $env:JASYPT_ENCRYPTOR_ALGORITHM"
# Checkmarx properties
Write-Host "Checkmarx URI :: $CHECKMARX_URI"
Write-Debug "Checkmarx User :: $CHECKMARX_USER"
Write-Host "Checkmarx Project :: $CHECKMARX_PROJECT"
# Azure properties
Write-Debug "Azure URL :: $AZURE_URL"
Write-Host "Azure Project :: $AZURE_PROJECT"
Write-Host "Azure Branch :: $AZURE_BRANCH"
Write-Debug "Azure Team :: $AZURE_TEAM"


# This will execute CxFlow will settings from the Azure pipeline
java -jar "${CXFLOW_JAR}" `
    -Xms512m -Xmx2048m `
    --spring.config.location=$CXFLOW_CONFIG `
    --${CXFLOW_MODE} `
    --app="$AZURE_PROJECT" `
    --namespace="$AZURE_TEAM" `
    --repo-name="$AZURE_PROJECT" `
    --branch="$AZURE_BRANCH" `
    --cx-project="$CHECKMARX_PROJECT" `
    --checkmarx.base-url="$CHECKMARX_URI" `
    --checkmarx.username="$CHECKMARX_USER" `
    --checkmarx.password="$CHECKMARX_PASSWORD" `
    --cx-flow.break-build="$CXFLOW_BREAK" `
    --azure.url="$AZURE_URL" `
    --azure.issue-type="$AZURE_BUGTYPE" `
    --bug-tracker="Azure" `
    --f="$CXFLOW_PATH"

Write-Host "CxFlow exiting..."
