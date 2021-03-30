param(
    [Parameter(Mandatory=$true)]
    [hashtable]$session,
    [Parameter(Mandatory=$true)]
    [string]$scan_settings_uri
)

. "support/rest_util.ps1"

$request_url = New-Object System.UriBuilder($session.base_url)
$request_url.Path = "cxrestapi$scan_settings_uri"

Write-Debug "scanSettings URL: $request_url"

$headers = GetRestHeadersForJsonRequest($session)

Invoke-RestMethod -Method 'Get' -Uri $request_url.Uri -Headers $headers


