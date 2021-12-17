param(
    [Parameter(Mandatory=$true)]
    [hashtable]$session,
    [Parameter(Mandatory=$true)]
    [string]$projectId,
    [string]$last,
    [int]$chunkSize=100
)


. "$PSScriptRoot/../../rest_util.ps1"

$request_url = New-Object System.Uri $session.base_url, "/cxrestapi/osa/scans"
$request_url = New-Object System.UriBuilder $request_url


# TODO: this should eventually return $last number of scans but use $chunkSize to calculate page number

$request_url.Query = GetQueryStringFromHashtable @{
    projectId=$projectId;
    itemsPerPage=$last;
}

Write-Debug "Scans API URL: $request_url"

$headers = GetRestHeadersForJsonRequest($session)

Invoke-RestMethod -Method 'Get' -Uri $request_url.Uri -Headers $headers

