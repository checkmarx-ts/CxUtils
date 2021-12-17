param(
    [Parameter(Mandatory=$true)]
    [hashtable]$session,
    [Parameter(Mandatory=$true)]
    [string]$project_name,
    [Parameter(Mandatory=$true)]
    [string]$owning_team,
    [boolean]$isPublic=$true
)

. "$PSScriptRoot/../../../rest_util.ps1"

$request_url = New-Object System.Uri($session.base_url, "/cxrestapi/projects")

Write-Debug "Create projects URL: $request_url"

$headers = GetRestHeadersForJsonRequest($session)

$payload = @{
    name = $project_name
    owningTeam = $owning_team
    isPublic = $isPublic
}

Invoke-RestMethod -Method 'Post' -Uri $request_url -Headers $headers -Body $payload

