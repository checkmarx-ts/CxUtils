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
    C:\PS> .\cxInsight_8_9.ps1 -cx_sast_server https://customerurl.checkmarx.net
.EXAMPLE
    C:\PS> .\cxInsight_8_9.ps1 -start_date 2019-04-01
.EXAMPLE
    C:\PS> .\cxInsight_8_9.ps1 -cx_sast_server http://localhost -day_span 180
.NOTES
    Author: Checkmarx
    Date:   April 13, 2020
#>

param(
    [Parameter(Mandatory=$true)]
    [String]$cx_sast_server,
    [int]$day_span = 90,
    [String]$start_date = ((Get-Date).AddDays(-$day_span).ToString("yyyy-MM-dd")),
    [String]$end_date = (Get-Date -format "yyyy-MM-dd")
    ) 
 
###### Do Not Change The Following Configs ######
$grantType = "password"
$scope = "sast_rest_api"
$clientId = "resource_owner_client"
$clientSecret = "014DF517-39D1-4453-B7B3-9930C563627C"

$cred = Get-Credential -Credential $null
$cxUsername = $cred.UserName
$pscred = $cred.GetNetworkCredential()
$cxPassword = $cred.GetNetworkCredential().password
 
$body = @{
    username = $cxUsername
    password = $cxPassword
    grant_type = $grantType
    scope = $scope
    client_id = $clientId
    client_secret = $clientSecret
}

$Url = "${cx_sast_server}/cxwebinterface/odata/v1/Scans?`$select=Id,ProjectName,OwningTeamId,TeamName,ProductVersion,EngineServerId,Origin,PresetName,ScanRequestedOn,QueuedOn,EngineStartedOn,EngineFinishedOn,ScanCompletedOn,ScanDuration,FileCount,LOC,FailedLOC,TotalVulnerabilities,High,Medium,Low,Info,IsIncremental,IsLocked,IsPublic&`$expand=ScannedLanguages(`$select=LanguageName)&`$filter=ScanRequestedOn%20gt%20${start_date}Z%20and%20ScanRequestedOn%20lt%20${end_date}z"
 
try {
    $response = Invoke-RestMethod -uri $cx_sast_server/cxrestapi/auth/identity/connect/token -method post -body $body -contenttype 'application/x-www-form-urlencoded'
} catch {
    Write-Host "StatusCode:" $_.Exception.Response.StatusCode.value__
    Write-Host "StatusDescription:" $_.Exception.Response.StatusDescription
    Write-Host ""
    Write-Host ""
    Write-Host $Url
    Read-Host -Prompt "An Error has prevented this script from being successful. Press paste the above Odata query in your browser..."
    throw "Could not authenticate"
}

try
{
    
    $response = Invoke-WebRequest -Uri $Url -Credential $cred -OutFile data.txt -ErrorAction Stop
    # This will only execute if the Invoke-WebRequest is successful.
    $StatusCode = $Response.StatusCode
    Read-Host -Prompt "The script was successful. Please send the 'data.txt' file in this directory to your Checkmarx Engineer. Press Enter to exit"
}
catch
{
    Write-Error $_.Exception.ToString()
    Write-Host "StatusCode:" $_.Exception.Response.StatusCode.value__ 
    Write-Host "StatusDescription:" $_.Exception.Response.StatusDescription
    Write-Host ""
    Write-Host ""
    Write-Host $Url
    Read-Host -Prompt "An Error has prevented this script from being successful. Press paste the above Odata query in your browser..."
}

