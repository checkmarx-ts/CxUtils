param(
    [Parameter(Mandatory=$true)]
    [hashtable]$session,
    [Parameter(Mandatory=$true)]
    [string]$project_id,
    [Parameter(Mandatory=$true)]
    [hashtable]$body
)

. "support/rest_util.ps1"

$path = "/cxrestapi/projects/$project_id"

$request_url = New-Object System.Uri $session.base_url, $path

Write-Debug "Projects API URL: $request_url"

$headers = GetRestHeadersForJsonRequest($session, "2.0")

Invoke-RestMethod -Method 'Put' -Uri $request_url -Headers $headers -ContentType "application/json" -Body $($body | ConvertTo-Json)

