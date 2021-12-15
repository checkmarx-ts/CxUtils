param(
    [Parameter(Mandatory=$true)]
    [hashtable]$session,
    [Parameter(Mandatory=$true)]
    $project_id,
    [Parameter(Mandatory=$true)]
    $preset_id,
    [Parameter(Mandatory=$true)]
    $engine_config_id,
    [string[]]$failed_scan_emails,
    [string[]]$before_scan_emails,
    [string[]]$after_scan_emails
)

. "$PSScriptRoot/../../../rest_util.ps1"

$request_url = New-Object System.Uri($session.base_url, "/cxrestapi/sast/scanSettings")

Write-Debug "scanSettings URL: $request_url"

$payload = [ordered]@{
    projectId = $project_id
    presetId = $preset_id
    engineConfigurationId = $engine_config_id
    emailNotifications = @{
        failedScan = $failed_scan_emails
        beforeScan = $before_scan_emails
        afterScan = $after_scan_emails
    }
}

$json = $($payload | ConvertTo-Json)


$headers = GetRestHeadersForJsonRequest($session)

Invoke-RestMethod -Method 'Post' -Uri $request_url -Headers $headers -Body $json -ContentType "application/json" 



