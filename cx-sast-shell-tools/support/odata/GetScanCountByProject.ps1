[Parameter(Mandatory=$true)]
[hashtable]$session


. "$PSScriptRoot/../rest_util.ps1"

$query = "/cxwebinterface/odata/v1/Projects?`$select=Id,OwningTeamId,Name&`$filter=TotalProjectScanCount eq 0"

$url = New-Object System.Uri $session.base_url, $query


$h = GetRestHeadersForJsonRequest($session)


try {
    Invoke-RestMethod -Method 'GET' -Uri $url -Headers $h
}
catch {
    Write-Output "$url returned code:" $_.Exception.Response.StatusCode.value__
    return $null
}
