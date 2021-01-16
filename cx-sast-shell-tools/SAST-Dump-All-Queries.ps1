param(
    [Parameter(Mandatory = $true)]
    [System.Uri]$sast_url,
    [Parameter(Mandatory = $true)]
    [String]$username,
    [Parameter(Mandatory = $true)]
    [String]$password,
    [Switch]$dbg
)

. "support/debug.ps1"

setupDebug($dbg.IsPresent)

$session = &"support\rest\sast\login.ps1" $sast_url $username $password -dbg:$dbg.IsPresent -soap_login_script "support/soap/audit/login.ps1"

try {
    $response = &"support\soap\audit\getquerycollection.ps1" $session
}
catch {
    throw $_
}
finally {
    $logout = &"support\soap\audit\logout.ps1" $session
    if ($true -ne $logout) {
        Write-Output WARNING - Logout failed.
    }
}

$response | Out-File -Encoding "UTF8" "CxQL_queries.xml"
