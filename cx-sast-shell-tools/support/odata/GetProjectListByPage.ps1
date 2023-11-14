param(
[Parameter(Mandatory=$true)]
[hashtable]$session,
[Parameter(Mandatory=$true)]
[int]$pageSize,
[string]$afterId=$null
)

. "$PSScriptRoot/../rest_util.ps1"

$query = "/cxwebinterface/odata/v1/Projects?`$select=OwningTeamId,Id,Name&`$orderby=Id asc&`$top=$($pageSize)&`$expand=LastScan(`$select=Id,ScanCompletedOn)"

if (-not $null -eq $afterId) {
    $query = $query + "&`$filter=id gt $($afterId)"
}

$url = New-Object System.Uri $session.base_url, $query

$h = GetRestHeadersForJsonRequest($session)


try {
    Invoke-RestMethod -Method 'GET' -Uri $url -Headers $h
}
catch {
    Write-Output "$url returned code:" $_.Exception.Response.StatusCode.value__
    return $null
}
