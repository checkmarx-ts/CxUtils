param(
    [Parameter(Mandatory=$true)]
    [hashtable]$session
)

. "$PSScriptRoot/../../rest_util.ps1"

$request_url = New-Object System.Uri $session.base_url, "/cxrestapi/sast/presets"

Write-Debug "Presets API URL: $request_url"

$headers = GetRestHeadersForJsonRequest($session)

Invoke-RestMethod -Method 'Get' -Uri $request_url -Headers $headers

