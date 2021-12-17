param(
    [Parameter(Mandatory=$true)]
    [hashtable]$session,
    [Parameter(Mandatory = $true)]
    [string]$project_id
)

. "$PSScriptRoot/../../rest_util.ps1"

$request_url = New-Object System.Uri $session.base_url, "/cxrestapi/projects/$project_id/sourceCode/excludeSettings"

Write-Debug "Exclude Settings API URL: $request_url"

$headers = GetRestHeadersForJsonRequest($session)

Invoke-RestMethod -Method 'Get' -Uri $request_url -Headers $headers

