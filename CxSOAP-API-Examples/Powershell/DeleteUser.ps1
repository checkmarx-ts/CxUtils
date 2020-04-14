######## Checkmarx Config ########
#Install-Module -Name "CredentialManager"
$credentials = Get-StoredCredential -Target "CxPortal" –AsCredentialObject
 
$domain = "http://localhost"
$username = $credentials.UserName
$password = $credentials.Password

$userEmailToDelete = "reviewer.none@cx"

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
######## Get All Users ########
function getUsers($proxy, $sessionId){
    $res = $proxy.GetAllUsers($sessionId)
    if($res.IsSuccesfull){
        return $res.UserDataList
    } else{
        Write-Host "Failed to Get Users : " $res.ErrorMessage
        exit 1
    }
}

function getUserIdByEmail($proxy, $sessionId, $email){
    $users = getUsers $proxy $sessionId
    foreach($user in $users){
        if($user.Email -eq $email){
            return $user.ID
        }
    }
    Write-Error "User ${email} was not found"
    exit 1
}
######## Delete User By ID ########
function deleteUserById($proxy, $sessionId, $userId){
    $res = $proxy.DeleteUser($sessionId, $userId)
    if($res.IsSuccesfull){
        return $res.IsSuccesfull
    } else{
        Write-Host "Failed to Delete User ${userId} : " $res.ErrorMessage
        exit 1
    }
}
$proxy = getProxy $domain
$sessionId = login $proxy $username $password

$userIdToDelete = getUserIdByEmail $proxy $sessionId $userEmailToDelete
$userDeleted = deleteUserById $proxy $sessionId $userIdToDelete

Write-Host "User ${userEmailToDelete} deleted with success"