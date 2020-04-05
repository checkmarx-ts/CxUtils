<#
.SYNOPSIS
An example of how to call the CxSAST REST API with OAuth2 Authentication.

.DESCRIPTION
Fetches engine server information using CxSAST REST API w/ OAuth2 AuthN method.

.PARAMETER server
The protocol and hostname of the Cx Manager server that hosts the API. examples: "http://localhost", "https://sast.example.com"

.PARAMETER cxUsername
The name of the user to connect to API. 

.PARAMETER cxPassword
The password of the user

.EXAMPLE
rest-api-example.ps1 -server "localhost" -cxUsername "user" -cxPassword "password"
#>

param(
    [Parameter(Mandatory = $true)][String]$server,
    [Parameter(Mandatory = $true)][String]$cxUsername,
    [Parameter(Mandatory = $true)][String]$cxPassword
)

 

# Login to the REST API via OAuth2 flow and return bearer token
function getOAuth2Token($serverRestEndpoint, $cxUsername, $cxPassword){
    $body = @{
        username = $cxUsername
        password = $cxPassword
        grant_type = "password"
        scope = "sast_rest_api"
        client_id = "resource_owner_client"
        client_secret = "014DF517-39D1-4453-B7B3-9930C563627C"
    }
     
    try {
        $response = Invoke-RestMethod -uri "${serverRestEndpoint}auth/identity/connect/token" -method post -body $body -contenttype 'application/x-www-form-urlencoded'
    } catch {
        Write-Host "StatusCode:" $_.Exception.Response.StatusCode.value__
        Write-Host "StatusDescription:" $_.Exception.Response.StatusDescription
        throw "Cannot Get OAuth2 Token"
    }
     
    return $response.token_type + " " + $response.access_token
}

# Fetch engine information from REST API using bearer token
function getEngineServers($serverRestEndpoint, $token){
    $headers = @{
        Authorization = $token
    }
    try {
        $response = Invoke-RestMethod -uri "${serverRestEndpoint}sast/engineServers" -method get -headers $headers
        return $response
    } catch {
        Write-Host "StatusCode:" $_.Exception.Response.StatusCode.value__
        Write-Host "StatusDescription:" $_.Exception.Response.StatusDescription
        throw "Cannot Get Engine Servers"
    }
}


$serverRestEndpoint = $server + "/cxrestapi/"

# Login
$token = getOAuth2Token $serverRestEndpoint $cxUsername $cxPassword

# Make API Call
$engineServers = getEngineServers $serverRestEndpoint $token

# Write data to console
$engineServers | ConvertTo-Json
