param(
    [Parameter(Mandatory=$true)]
    [hashtable]$session,
    [Parameter(Mandatory=$true)]
    [string]$scanId,
    [int]$chunkSize=100
)


. "$PSScriptRoot/../../rest_util.ps1"

$request_url = New-Object System.Uri $session.base_url, "/cxrestapi/osa/libraries"
$request_url = New-Object System.UriBuilder $request_url

$headers = GetRestHeadersForJsonRequest($session)

$curPage = 1

$libs =  [System.Collections.ArrayList]@()

while($true) {
    $request_url.Query = GetQueryStringFromHashtable @{
        scanId=$scanId;
        page=$curPage;
        itemsPerPage=$chunkSize;
    }

    Write-Debug "Scans API URL: $request_url"

    $response = Invoke-RestMethod -Method 'Get' -Uri $request_url.Uri -Headers $headers
    $curPage++

    foreach($responseLib in $response) {
        $libs.Add("$($responseLib.name):$($responseLib.version)") | Out-Null
    }

    if ($response.count -lt $chunkSize) {
        break
    }
}

$libs

