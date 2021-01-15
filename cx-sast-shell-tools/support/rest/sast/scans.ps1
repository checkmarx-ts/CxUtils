param(
    [Parameter(Mandatory=$true)]
    [hashtable]$session,
    [Parameter(Mandatory=$true)]
    [string]$projectId,
    [string]$scanStatus="Finished",
    [string]$last="1"
)

. "support/rest_util.ps1"

$request_url = New-Object System.Uri $session.base_url, "/cxrestapi/sast/scans"
$request_url = New-Object System.UriBuilder $request_url

$request_url.Query = GetQueryStringFromHashtable @{
    projectId=$projectId;
    scanStatus=$scanStatus;
    last=$last;
}

Write-Debug "Scans API URL: $request_url"

$headers = GetRestHeadersForJsonRequest($session)

Invoke-RestMethod -Method 'Get' -Uri $request_url.Uri -Headers $headers

