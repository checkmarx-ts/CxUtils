param(
    [Parameter(Mandatory=$true)]
    [hashtable]$session,
    [string]$project_id,
    [string]$api_version="2.0"
)

. "$PSScriptRoot/../../rest_util.ps1"

$path = "/cxrestapi/projects"

if ([String]::IsNullOrEmpty($project_id) -ne $true) {
    $path += "/$project_id"
}

$request_url = New-Object System.Uri $session.base_url, $path

Write-Debug "Projects API URL: $request_url"

$headers = GetRestHeadersForJsonRequest $session $api_version

Invoke-RestMethod -Method 'Get' -Uri $request_url -Headers $headers

