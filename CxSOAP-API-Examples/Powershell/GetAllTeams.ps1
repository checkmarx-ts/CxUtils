######## Checkmarx Config ########
#Install-Module -Name "CredentialManager"
$credentials = Get-StoredCredential -Target "CxPortal" –AsCredentialObject
 
$domain = "http://localhost"
$username = $credentials.UserName
$password = $credentials.Password

######## Get Proxy ########
function getProxy($domain){
    return New-WebServiceProxy -Uri ${domain}/CxWebInterface/Portal/CxWebService.asmx?wsdl
}
######## Login ########
function login($proxy, $user, $pass){
    $proxyType = $proxy.gettype().Namespace

    $credentials = new-object ("$proxyType.Credentials")
    $credentials.User = $user
    $credentials.Pass = $pass
    $res = $proxy.Login($credentials, 1033) 
    
    if($res.IsSuccesfull){
        return $res.SessionId
    } else{
        Write-Host "Login Failed : " $res.ErrorMessage
        exit 1
    }
}
######## Get All Teams ########
function getTeams($proxy, $sessionId){
    $res = $proxy.GetAllTeams($sessionId)
    if($res.IsSuccesfull){
        return $res.TeamDataList
    } else{
        Write-Host "Failed to Get Teams : " $res.ErrorMessage
        exit 1
    }
}

$proxy = getProxy $domain
$sessionId = login $proxy $username $password
$teams = getTeams $proxy $sessionId
($teams | ConvertTo-Json -Depth 99)