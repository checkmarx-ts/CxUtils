<#
.SYNOPSIS
This is a Powershell script to retrieve your Checkmarx ScanData for Insight Analysis
.DESCRIPTION
This script will collect Scan Information that includes data about: Projects, Presets, Teams, Engines, and Result Metrics. It also optionally retrieves scan results and generates a summary of them.
.PARAMETER cx_sast_server
    URL of the Checkmarx Server (i.e. https://companyname.checkmarx.net or http://localhost).
.PARAMETER day_span
    The amount of days you from current day you would like to retrieve data for.
.PARAMETER start_date
    The start date of the date range you would like to collect data (Format: yyyy-mm-DD)
.PARAMETER end_date
    The end date of the date range you would like to collect data (Format: yyyy-mm-DD)
.PARAMETER bypassProxy
    If provided, the script will attempt to bypass any proxy when invoking the CxSAST API
.PARAMETER Results
    If provided, the script will retrieve and summarize result data as well as scan data. Either this option or the -ExclResults option must be provided.
.PARAMETER ExclResults
    If provided, the script will not retrieve result data. Either this option or the -Results option must be provided.
.PARAMETER ExclProjectName
    If provided, the project name will be excluded from the scan results.
.PARAMETER ExclTeamName
    If provided, the team name will be excluded from the scan results.
.PARAMETER ExclAll
    If provided, the project name and the team name will be excluded from the scan results, and the result data will not be retrieved.
.PARAMETER verbose
    If provided, the script will retrieve print activity messages
.EXAMPLE
    C:\PS> .\cxInsight_9_0.ps1 -cx_sast_server https://customerurl.checkmarx.net -exclresults
.EXAMPLE
    C:\PS> .\cxInsight_9_0.ps1 -start_date 2019-04-01 -exclresults
.EXAMPLE
    C:\PS> .\cxInsight_9_0.ps1 -cx_sast_server http://localhost -day_span 180 -exclresults
.EXAMPLE
    C:\PS> .\cxInsight_9_0.ps1 -cx_sast_server http://localhost -results
.EXAMPLE
    C:\PS> .\cxInsight_9_0.ps1 -cx_sast_server http://localhost -exclall
.NOTES
    Author: Checkmarx
    Date:   April 13, 2020
    Updated: July 28, 2025
#>

param(
    [Parameter(Mandatory=$true)]
    [System.URI]$cx_sast_server,
    [int]$day_span = 90,
    [String]$start_date = ((Get-Date).AddDays(-$day_span).ToString("yyyy-MM-dd")),
    [String]$end_date = (Get-Date -format "yyyy-MM-dd"),
    [Parameter(Mandatory=$False)]
    [switch]
    $bypassProxy,
    [Parameter(Mandatory=$False)]
    [switch]
    $results,
    [Parameter(Mandatory=$False)]
    [switch]
    $exclresults,
    [Parameter(Mandatory=$False)]
    [switch]
    $exclProjectName,
    [Parameter(Mandatory=$False)]
    [switch]
    $exclTeamName,
    [Parameter(Mandatory=$False)]
    [switch]
    $exclAll
    )

if (($cx_sast_server.Scheme -ne "http") -and ($cx_sast_server.Scheme -ne "https")) {
    Write-Error "SAST server URL must start with http:// or https://"
    exit
}

if ($cx_sast_server.PathAndQuery -ne "/") {
    Write-Host "Truncating path and query (`"$($cx_sast_server.PathAndQuery)`") from SAST server URL"
    $Builder = [System.URIBuilder]::New(
        $cx_sast_server.Scheme,
        $cx_sast_server.Host,
        $cx_sast_server.Port
    )
    $cx_sast_server = [System.URI]::New($Builder)
    Write-Host "SAST server URL is now $cx_sast_server"
}

if ( ! ( $results -or $exclresults -or $exclAll ) ) {
    Write-Error "Either -Results, -ExclResults or -ExclAll must be provided"
    exit
}

if ( $exclResults -or $exclAll ) {
    if ( $results ) {
        Write-Warning "The -ExclResults and -ExclAll options take precedence over the -Results option"
        $results = $null
    }
}

# Make sure start and end date have been provided in the correct
# format
try {
    $tmp = [datetime]::ParseExact($start_date, "yyyy-MM-dd", $null)
    $tmp = [datetime]::ParseExact($end_date, "yyyy-MM-dd", $null)
} catch {
    Write-Error "Start and end dates must be in YYYY-MM-DD format"
    exit
}

###### Do Not Change The Following Configs ######
$grantType = "password"
$scope = "access_control_api sast_api"
$clientId = "resource_owner_sast_client"
$clientSecret = "014DF517-39D1-4453-B7B3-9930C563627C"

$cred = Get-Credential -Credential $null
$cxUsername = $cred.UserName
$cxPassword = $cred.GetNetworkCredential().password

# Data exclusion
$projectName = "ProjectName,"
$teamName = "TeamName,"

if ( $exclProjectName -or $exclAll ) {
    $projectName = ""
}
if ( $exclTeamName -or $exclAll ) {
    $teamName = ""
}

function getOAuth2Token() {
    $body = @{
        username      = $cxUsername
        password      = $cxPassword
        grant_type    = $grantType
        scope         = $scope
        client_id     = $clientId
        client_secret = $clientSecret
    }

    $cxargs = @{
        Uri = [System.URI]::New($cx_sast_server, "/cxrestapi/auth/identity/connect/token")
        Method = "Post"
        Body = $body
        ContentType =  "application/x-www-form-urlencoded"
    }
    if ($bypassProxy) {
        $cxargs.NoProxy = $true
    }

    Write-Verbose "Retrieving OAuth2 token"
    Write-Verbose "Url: $($cxargs.Uri)"
    try {
        $response = Invoke-RestMethod @cxargs
    }
    catch {
        Write-Host "Exception:" $_
        Write-Host "StatusCode:" $_.Exception.Response.StatusCode.value__
        Write-Host "StatusDescription:" $_.Exception.Response.StatusDescription
		Write-Host "Unable to retrieve Checkmarx AC Token"
        exit(-1)
    }

    return $response.token_type + " " + $response.access_token
}

Write-Host "Running Script on Version " (get-host).Version
$token = getOAuth2Token

function odata() {
    param (
        $Uri,
        $OutFile
    )

    $headers = @{
        Authorization = $token
    }
    $cxargs = @{
        Uri = $Uri
        Headers = $headers
        Method = "Get"
    }
    if ($AllowUnencryptedAuthenticationresults) {
        $cxargs.AllowUnencryptedAuthentication = $true
    }
    if ($bypassProxy) {
        $cxargs.NoProxy = $true
    }
    if ($OutFile) {
        $cxargs.OutFile = $OutFile
    }

    return Invoke-RestMethod @cxargs
}

function getScanOdata {
    param (
        $fileList,
        [Version]$version
    )

    $outputFile = ".\scan-data.json"
    Write-Verbose "Retrieving scan data"

    # The OData API is annoying: if we request a field that doesn't
    # exist, it won't fail, it will just return the wrong data.
    $Critical = ""
    if (($Version.Major -eq 9) -and ($Version.Minor -ge 7)) {
        $Critical = "Critical,"
    }

    $Url = [System.URI]::New($cx_sast_server, "/cxwebinterface/odata/v1/Scans?`$select=Id,ProjectId,${ProjectName}OwningTeamId,${TeamName}ProductVersion,EngineServerId,Origin,PresetName,ScanRequestedOn,QueuedOn,EngineStartedOn,EngineFinishedOn,ScanCompletedOn,ScanDuration,FileCount,LOC,FailedLOC,TotalVulnerabilities,${Critical}High,Medium,Low,Info,IsIncremental,IsLocked,IsPublic&`$expand=ScannedLanguages(`$select=LanguageName),Project(`$select=EngineConfigurationId;`$expand=EngineConfiguration)&`$filter=ScanRequestedOn%20gt%20${start_date}Z%20and%20ScanRequestedOn%20lt%20${end_date}z")
    Write-Verbose "`$Url: $Url"
    try {
        $response = odata -Uri $Url -OutFile $outputFile
        [void]$fileList.Add($outputFile)
    }
    catch {
        Write-Host "Exception:" $_ -ForegroundColor "Red"
        Write-Host $_.ScriptStackTrace -ForegroundColor "DarkGray"
        Write-Host "StatusCode:" $_.Exception.Response.StatusCode.value__
        Write-Host "StatusDescription:" $_.Exception.Response.StatusDescription
        Write-Host $Url
        Write-Host "An error has prevented this script from collecting scan Odata."
    }
}

function getResultOData {
    param (
        $fileList
    )

    $outputFile = ".\result-data.json"
    Write-Verbose "Retrieving result data"

    $Url = [System.URI]::New($cx_sast_server, "/cxwebinterface/odata/v1/Projects?`$select=Id,LastScanId")
    Write-Verbose "`$Url: $Url"
    try {
        $response = odata -Uri $Url
        $projects = @{}
        $response | Select-Object -ExpandProperty Value | ForEach-Object {
            $projectId = "$($_.Id)"
            $lastScanId = $_.LastScanId

            if (-Not $lastScanId) {
                Write-Verbose "Project ${projectId} has no last scan"
                return
            }

            Write-Progress -Activity "Retrieving Results" -Status "Retrieving result data for scan ${lastScanId} (project ${projectId})"
            Write-Verbose "Retrieving result data for scan ${lastScanId} (project ${projectId})"

            $Url = [System.URI]::New($cx_sast_server, "/cxwebinterface/odata/v1/Scans?`$filter=Id%20eq%20${lastScanId}%20and%20ScanRequestedOn%20gt%20${start_date}Z%20and%20ScanRequestedOn%20lt%20${end_date}z&`$select=Id&`$expand=Results(`$select=Id,ScanId,ResultId,StateId;`$expand=State)")
            Write-Verbose "URL is ${Url}"

            $response = odata -Uri $Url
            if (-Not $Response.Value) {
                Write-Verbose "No matching scan found in the specified date range for project ${projectId}"
                return
            }

            $response | Select-Object -ExpandProperty Value | ForEach-Object {
                if ( -not $projects.ContainsKey($projectId) ) {
                    $projects[$projectId] = @{
                        LastScanId = ${lastScanId}
                        Results = @{}
                    }
                }

                Foreach ( $result in $_.Results ) {
                    $stateId = "$($result.StateId)"
                    $stateName = "$($result.State.Name)"
                    $projects[$projectId]['Results'][$stateName] = $projects[$projectId]['Results'][$stateName] + 1
                }
            }
        }

        # Convert projects hashmap to an array
        $newProjects = @()
        Foreach ( $projectId in $projects.Keys ) {
            $project = @{
                ProjectId = $projectId
                LastScanId = $projects.$projectId.LastScanId
                Results = @()
            }
            Foreach ( $stateName in $projects.$projectId.Results.Keys ) {
                $result = @{
                    StateName = $stateName
                    Count = $projects.$projectId.Results.$stateName
                }
                $project.Results += $result
            }
            $newProjects += $project
        }

        $response = @{
            "Projects" = $newProjects
        }

        $response | ConvertTo-Json -Compress -Depth 4 | Out-File -FilePath $outputFile -Encoding utf8
        [void]$fileList.Add($outputFile)
    }
    catch {
        Write-Host "Exception:" $_
        Write-Host "StatusCode:" $_.Exception.Response.StatusCode.value__
        Write-Host "StatusDescription:" $_.Exception.Response.StatusDescription
        Write-Host $Url
        Write-Host "An error has prevented this script from collecting result Odata."
    }
}

function getLicenseData {
    param (
        $fileList
    )

    $outputFile = ".\license-data.json"
    Write-Verbose "Retrieving license data"

    $Url = [System.URI]::New($cx_sast_server, "/cxrestapi/serverLicenseData")
    Write-Verbose "`$Url: $Url"
    try {
        $response = odata -Uri $Url -OutFile $outputFile
        [void]$fileList.Add($outputFile)
    }
    catch {
        if ($_.Exception.Response.StatusCode.value__ -eq 404) {
            Write-Host "Server license data not available"
        } else {
            Write-Host "Exception:" $_ -ForegroundColor "Red"
            Write-Host $_.ScriptStackTrace -ForegroundColor "DarkGray"
            Write-Host "StatusCode:" $_.Exception.Response.StatusCode.value__
            Write-Host "StatusDescription:" $_.Exception.Response.StatusDescription
            Write-Host $Url
            Write-Host "An error has prevented this script from collecting license data."
        }
    }
}

function getEngineData {
    param (
        $fileList
    )

    $outputFile = ".\engine-data.json"
    Write-Verbose "Retrieving engine data"

    $Url = [System.URI]::New($cx_sast_server, "/cxrestapi/sast/engineServers")
    Write-Verbose "`$Url: $Url"
    try {
        $response = odata -Uri $Url -OutFile $outputFile
        [void]$fileList.Add($outputFile)
    }
    catch {
        Write-Host "Exception:" $_ -ForegroundColor "Red"
        Write-Host $_.ScriptStackTrace -ForegroundColor "DarkGray"
        Write-Host "StatusCode:" $_.Exception.Response.StatusCode.value__
        Write-Host "StatusDescription:" $_.Exception.Response.StatusDescription
        Write-Host $Url
        Write-Host "An error has prevented this script from collecting license data."
        return $false
    }
}

function getSASTVersion {

    Write-Verbose "Retrieving SAST version"

    $Url = [System.URI]::New($cx_sast_server, "/cxrestapi/system/version")
    Write-Verbose "`$Url: $Url"
    try {
        $response = odata -Uri $Url
    }
    catch {
        Write-Host "Exception:" $_ -ForegroundColor "Red"
        Write-Host $_.ScriptStackTrace -ForegroundColor "DarkGray"
        Write-Host "StatusCode:" $_.Exception.Response.StatusCode.value__
        Write-Host "StatusDescription:" $_.Exception.Response.StatusDescription
        Write-Host $Url
        Write-Host "An error has prevented this script from retrieving the system version."
        return $false
    }
    return $response
}

class Version {
    [int]$Major
    [int]$Minor
    [int]$Patch
    [int]$Build
    [int]$EnginePack
    [int]$EnginePackPatch

    Version([object]$data) {
        $this.Major, $this.Minor, $this.Patch, $this.Build = $data.Version -split '\.'
        # The enginePackVersion property was added to the JSON response in CxSAST 9.5.
        if ($data.PSObject.Properties.Name -contains "EnginePackVersion") {
            $_, $_, $this.EnginePack, $this.EnginePackPatch = $data.EnginePackVersion -split '\.'
        } else {
            $this.EnginePack = $null
            $this.EnginePackPatch = $null
        }
    }

    [string]ToString() {
        return "Version[Major=$($this.Major),Minor=$($this.Minor),Patch=$($this.Patch),Build=$($this.Build),EnginePack=$($this.EnginePack),EnginePackPatch=$($this.EnginePackPatch)]"
    }
}

try
{
    $files = [System.Collections.ArrayList]::new()
    $data = getSASTVersion
    $version = [Version]::New($data)
    Write-Host "$version"
    getScanOdata $files $version
    getEngineData $files
    getLicenseData $files
    if ($results) {
        getResultOdata $files
    }
    # Compress-Archive was introduced in PowerShell version 5.
    if ($PSVersionTable.PSVersion.Major -gt 4) {
        Compress-Archive -Path $files -DestinationPath ".\data.zip" -Force
        Remove-Item -Path $files
        Read-Host -Prompt "The script was successful. Please send the 'data.zip' file in this directory to your Checkmarx Engineer. Press Enter to exit"
    }
    else {
        Read-Host -Prompt "The script was successful. Please send the ${files} file(s) in this directory to your Checkmarx Engineer. Press Enter to exit"
    }
}
catch
{
    Write-Host "Exception:" $_
    Write-Error $_.Exception.ToString()
    Write-Host "StatusCode:" $_.Exception.Response.StatusCode.value__
    Write-Host "StatusDescription:" $_.Exception.Response.StatusDescription
    Read-Host -Prompt "The above error occurred. Press Enter to exit."
}
