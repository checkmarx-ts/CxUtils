param(
    [Parameter(Mandatory=$true)]
    [hashtable]$session,
    [Parameter(Mandatory=$true)]
    [string]$reportID
)

. "support/rest_util.ps1"

$rest_url = [String]::Format("/cxrestapi/reports/sastScan/{0}/status", $reportID)
$request_url = New-Object System.Uri $session.base_url, $rest_url


Write-Debug "Scans API URL: $request_url"

$headers = GetRestHeadersForJsonRequest($session)

Invoke-RestMethod -Method 'Get' -Uri $request_url -Headers $headers
