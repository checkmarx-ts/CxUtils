param(
    [Parameter(Mandatory=$true)]
    [hashtable]$session,
    [Parameter(Mandatory=$true)]
    [string]$project_id
)

. "$PSScriptRoot/../../../rest_util.ps1"

$path = "/cxrestapi/projects/$($project_id)"

$request_url = New-Object System.Uri $session.base_url, $path

Write-Debug "Projects API URL: $request_url"

$headers = GetRestHeadersForJsonRequest($session, "2.0")

Invoke-RestMethod -Method 'delete' -Uri $request_url -Headers $headers -Body '{ "deleteRunningScans" : true }' -ContentType "application/json"
