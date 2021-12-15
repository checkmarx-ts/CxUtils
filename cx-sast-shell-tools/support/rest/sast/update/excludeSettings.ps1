param(
    [Parameter(Mandatory=$true)]
    [hashtable]$session,
    [Parameter(Mandatory = $true)]
    [string]$project_id,
    [Parameter(Mandatory = $true)]
    [hashtable]$body

)

. "$PSScriptRoot/../../../rest_util.ps1"

$request_url = New-Object System.Uri $session.base_url, "/cxrestapi/projects/$project_id/sourceCode/excludeSettings"

Write-Debug "Exclude Settings API URL: $request_url"

$headers = GetRestHeadersForJsonRequest($session)

Invoke-RestMethod -Method 'Put' -Uri $request_url -Headers $headers -ContentType "application/json" -Body $($body | ConvertTo-Json)

