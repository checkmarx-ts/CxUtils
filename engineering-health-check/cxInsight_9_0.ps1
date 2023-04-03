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
    Updated: July 26, 2022
#>

param(
    [Parameter(Mandatory=$true)]
    [String]$cx_sast_server,
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

$serverRestEndpoint = $cx_sast_server + "/cxrestapi/"
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
        Uri = "${serverRestEndpoint}auth/identity/connect/token"
        Method = "Post"
        Body = $body
        ContentType =  "application/x-www-form-urlencoded"
    }
    if ($bypassProxy) {
        $cxargs.NoProxy = $true
    }

    Write-Verbose "Retrieving OAuth2 token"
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
        $fileList
    )

    $outputFile = ".\scan-data.json"
    Write-Verbose "Retrieving scan data"

    $Url = "${cx_sast_server}/cxwebinterface/odata/v1/Scans?`$select=Id,ProjectId,${ProjectName}OwningTeamId,${TeamName}ProductVersion,EngineServerId,Origin,PresetName,ScanRequestedOn,QueuedOn,EngineStartedOn,EngineFinishedOn,ScanCompletedOn,ScanDuration,FileCount,LOC,FailedLOC,TotalVulnerabilities,High,Medium,Low,Info,IsIncremental,IsLocked,IsPublic&`$expand=ScannedLanguages(`$select=LanguageName)&`$filter=ScanRequestedOn%20gt%20${start_date}Z%20and%20ScanRequestedOn%20lt%20${end_date}z"
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

    $Url = "${cx_sast_server}/cxwebinterface/odata/v1/Projects?`$select=Id,LastScanId"
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

            $Url = "${cx_sast_server}/cxwebinterface/odata/v1/Scans?`$filter=Id%20eq%20${lastScanId}%20and%20ScanRequestedOn%20gt%20${start_date}Z%20and%20ScanRequestedOn%20lt%20${end_date}z&`$select=Id&`$expand=Results(`$select=Id,ScanId,ResultId,StateId;`$expand=State)"
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

    $Url = "${cx_sast_server}/cxrestapi/serverLicenseData"
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

    $Url = "${cx_sast_server}/cxrestapi/sast/engineServers"
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

try
{
    $files = [System.Collections.ArrayList]::new()
    getScanOdata $files
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
