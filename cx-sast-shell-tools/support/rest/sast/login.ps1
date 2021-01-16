param(
    [System.Uri]$sast_url,
    [String]$username,
    [String]$password,
    [Switch]$dbg,
    [hashtable]$existing_session,
    [string]$soap_login_script = "support/soap/webinterface/login.ps1"
)

. "support/rest_util.ps1"

$session = @{}

if ($Null -ne $existing_session) {
    if (0 -ge [DateTime]::Compare($(Get-Date), $existing_session.expires_at)) {
        Write-Debug "Using existing login token"
        return $existing_session
    }
    else {
        Write-Debug "Refreshing login"
        $session = $existing_session
        $session.soap_session = & $soap_login_script $session.base_url $session.username $session.password
    }
}
else {
    Write-Debug "Executing new login"

    $query_elems = @{
        username      = $username;
        password      = $password;
        grant_type    = "password";
        client_secret = "014DF517-39D1-4453-B7B3-9930C563627C";
    }
    
    $soap_session = & $soap_login_script $sast_url $username $password
    
    if ($true -eq $soap_session.v9) {
        $query_elems.scope = "sast_api"
        $query_elems.client_id = "resource_owner_sast_client"
    }
    else {
        $query_elems.scope = "sast_rest_api"
        $query_elems.client_id = "resource_owner_client"
    }
    
    $api_path = "/cxrestapi/auth/identity/connect/token"
    
    $api_uri_base = New-Object System.Uri $sast_url, $api_path
    $api_uri = New-Object System.UriBuilder $api_uri_base

    $query = GetQueryStringFromHashtable $query_elems

    $session.reauth_uri  = $api_uri.Uri;
    $session.reauth_body = $query
    $session.username = $username
    $session.password = $password
    $session.soap_session = $soap_session
    $session.base_url = $sast_url
    
}

$resp = Invoke-RestMethod -Method 'Post' -Uri $session.reauth_uri -ContentType "application/x-www-form-urlencoded" -Body $session.reauth_body

$session.auth_header = [String]::Format("{0} {1}", $resp.token_type, $resp.access_token);
$session.expires_at  = $(Get-Date).AddSeconds($resp.expires_in);

return $session
