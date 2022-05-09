<#
.SYNOPSIS
This is a Powershell script to retrieve your Checkmarx ScanData for Insight Analysis
.DESCRIPTION
This script will collect Scan Information that includes data about: Projects, Presets, Teams, Engines, and Result Metrics
.PARAMETER cx_sast_server
    URL of the Checkmarx Server (i.e. https://companyname.checkmarx.net or http://localhost).
.PARAMETER day_span
    The amount of days you from current day you would like to retrieve data for.
.PARAMETER start_date
    The start date of the date range you would like to collect data (Format: yyyy-mm-DD)
.PARAMETER end_date
    The end date of the date range you would like to collect data (Format: yyyy-mm-DD)
.EXAMPLE
    C:\PS> .\cxInsight_9_0.ps1 -cx_sast_server https://customerurl.checkmarx.net
.EXAMPLE
    C:\PS> .\cxInsight_9_0.ps1 -start_date 2019-04-01
.EXAMPLE
    C:\PS> .\cxInsight_9_0.ps1 -cx_sast_server http://localhost -day_span 180
.NOTES
    Author: Checkmarx
    Date:   April 13, 2020
    Updated: March 9, 2021
#>

param(
    [Parameter(Mandatory=$true)]
    [String]$cx_sast_server,
    [int]$day_span = 90,
    [String]$start_date = ((Get-Date).AddDays(-$day_span).ToString("yyyy-MM-dd")),
    [String]$end_date = (Get-Date -format "yyyy-MM-dd"),
    [Parameter(Mandatory=$False)]
    [switch]
    $bypassProxy
    )

###### Do Not Change The Following Configs ######
$grantType = "password"
$scope = "access_control_api sast_api"
$clientId = "resource_owner_sast_client"
$clientSecret = "014DF517-39D1-4453-B7B3-9930C563627C"

$cred = Get-Credential -Credential $null
$cxUsername = $cred.UserName
$cxPassword = $cred.GetNetworkCredential().password

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

    try {
        if ($bypassProxy) {
            $response = Invoke-RestMethod -noProxy -uri "${serverRestEndpoint}auth/identity/connect/token" -method post -body $body -contenttype 'application/x-www-form-urlencoded'
        }
        else {
            $response = Invoke-RestMethod -uri "${serverRestEndpoint}auth/identity/connect/token" -method post -body $body -contenttype 'application/x-www-form-urlencoded'
        }
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

function getScanOdata {
    param (
        $outputFile
    )
    $Url = "${cx_sast_server}/cxwebinterface/odata/v1/Scans?`$select=Id,ProjectName,OwningTeamId,TeamName,ProductVersion,EngineServerId,Origin,PresetName,ScanRequestedOn,QueuedOn,EngineStartedOn,EngineFinishedOn,ScanCompletedOn,ScanDuration,FileCount,LOC,FailedLOC,TotalVulnerabilities,High,Medium,Low,Info,IsIncremental,IsLocked,IsPublic&`$expand=ScannedLanguages(`$select=LanguageName)&`$filter=ScanRequestedOn%20gt%20${start_date}Z%20and%20ScanRequestedOn%20lt%20${end_date}z"
    $headers = @{
        Authorization = $token
    }
    try {
        if ($bypassProxy) {
            $response = Invoke-RestMethod -noProxy -uri "$Url" -method get -headers $headers -OutFile $outputFile
        }
        else {
            $response = Invoke-RestMethod -uri "$Url" -method get -headers $headers -OutFile $outputFile
        }
    }
    catch {
        Write-Host "Exception:" $_
        Write-Host "StatusCode:" $_.Exception.Response.StatusCode.value__
        Write-Host "StatusDescription:" $_.Exception.Response.StatusDescription
	Write-Host $Url
	Write-Host "An error has prevented this script from collecting scan Odata."
        exit(-1)
    }
}

function getResultOData {
    param (
        $outputFile
    )

    $Url = "${cx_sast_server}/cxwebinterface/odata/v1/Projects?`$select=Id&`$expand=LastScan(`$select=Id;`$expand=Results(`$select=Id,ResultId,StateId))"
    $headers = @{
        Authorization = $token
    }
    try {
        if ($bypassProxy) {
            $response = Invoke-RestMethod -noProxy -uri "$Url" -method get -headers $headers
        }
        else {
            $response = Invoke-RestMethod -uri "$Url" -method get -headers $headers
        }

        $states = @{
            "0" = "To Verify"
            "1" = "Not Explotable"
            "2" = "Confirmed"
            "3" = "Urgent"
            "4" = "Proposed Not Exploitable"
        }
        $projects = @{}
        $totals = @{}
        $response | Select-Object -ExpandProperty Value | ForEach-Object {
            $projectId = "$($_.Id)"
            if ( -not $projects.ContainsKey($projectId) ) {
                $projects[$projectId] = @{}
            }

            $projects[$projectId]["LastScanId"] = $_.LastScan.Id
            Foreach ( $result in $_.LastScan.Results ) {
                $stateId = "$($result.StateId)"
                if ( -not $states.ContainsKey($stateId) ) {
                    $states[$stateId] = "Custom State $($result.StateId)"
                }
                $stateName = $states[$stateId]
                $projects[$projectId][$stateName] = $projects[$projectId][$stateName] + 1
                $totals[$stateName] = $totals[$stateName] + 1
            }
        }

        $response = @{
            "Projects" = $projects
            "Totals" = $totals
        }

        $response | ConvertTo-Json -Compress | Out-File -FilePath $outputFile
    }
    catch {
        Write-Host "Exception:" $_
        Write-Host "StatusCode:" $_.Exception.Response.StatusCode.value__
        Write-Host "StatusDescription:" $_.Exception.Response.StatusDescription
	Write-Host $Url
	Write-Host "An error has prevented this script from collecting result Odata."
        exit(-1)
    }
}

try
{
    $files = @(".\scan-data.json", ".\result-data.json")
    getScanOdata($files[0])
    getResultOdata($files[1])
    Compress-Archive -Path $files -DestinationPath ".\data.zip" -Force
    Remove-Item -Path $files
    Read-Host -Prompt "The script was successful. Please send the 'data.zip' file in this directory to your Checkmarx Engineer. Press Enter to exit"
}
catch
{
    Write-Host "Exception:" $_
    Write-Error $_.Exception.ToString()
    Write-Host "StatusCode:" $_.Exception.Response.StatusCode.value__
    Write-Host "StatusDescription:" $_.Exception.Response.StatusDescription
    Read-Host -Prompt "The above error occurred. Press Enter to exit."
}
