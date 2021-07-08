param(
    [Parameter(Mandatory=$true)]
    [hashtable]$session,
    [Parameter(Mandatory=$true)]
    [String]$reportid,
    [Parameter(Mandatory=$true)]
    [String]$teamName,
    [Parameter(Mandatory=$true)]
    [String]$projectName,
    [Parameter(Mandatory=$true)]
    [String]$outputPath
)

. "support/rest_util.ps1"

$rest_url = [String]::Format("/cxrestapi/reports/sastScan/{0}", $reportid)
$request_url = New-Object System.Uri $session.base_url, $rest_url

#adjust for windows slashes
$teamName = $teamName -replace "/", "\"
Write-Debug $teamName
$directory = [String]::Format("{0}\{1}", $outputPath, $teamName )
$date = Get-Date -Format "ddMMyyyy"
$fullpath = [String]::Format("{0}\{1}_{2}.pdf", $directory, $projectName, $date )
$pathExists = Test-Path -Path $directory
Write-Debug $fullpath

if($pathExists -eq $false){
    New-Item -ItemType Directory -Force -Path $directory
}

Write-Debug "Get Report API URL: $request_url"

$headers = GetRestHeadersForJsonRequest($session)

Invoke-RestMethod -Method 'Get' -Uri $request_url -Headers $headers -OutFile $fullpath
