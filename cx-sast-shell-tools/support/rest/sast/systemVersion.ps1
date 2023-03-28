param(
    [System.Uri]$sast_url
)

$api_path = "/cxrestapi/system/version"
    
$api_uri_base = New-Object System.Uri $sast_url, $api_path
$api_uri = New-Object System.UriBuilder $api_uri_base
Write-Host $api_uri.Uri
$resp = Invoke-RestMethod -Method 'GET' -Uri $api_uri.Uri
return $resp