######## Checkmarx Config ########
#Install-Module -Name "CredentialManager"
$credentials = Get-StoredCredential -Target "CxPortal" –AsCredentialObject
 
$domain = "http://localhost"
$username = $credentials.UserName
$password = $credentials.Password

$userEmail = "reviewer.none@cx" # Existing User
# Available User Types:
# Application
# Domain
# OpenID
# SAML
# SSO
# LDAP
# None
$userType = "Application"

$newTeamPath = "/CxServer/SP2/Company2/Team1" # Existing Team Path - Team Level

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
######## Get Team Full Path ########
function getTeamFullPath($proxy, $sessionId, $teamId){
    $res = $proxy.GetTeamFullPaths($sessionId, $teamId, $teamId)
    return $res.sourceTeamFullPath
}
function getTeamId($proxy, $sessionId, $teamPath){
    $teams = getTeams $proxy $sessionId
    foreach($team in $teams){
        $teamId = $team.Team.Guid
        $teamFullPath = getTeamFullPath $proxy $sessionId $teamId
        if($teamFullPath -eq $teamPath){
            return $teamId
        }
    }
    Write-Error "Failed to retrieve team ID of ${teamPath}"
    Write-Error "Team ${teamPath} might not exist"
    exit 1
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
######## Get User By ID ########
function getUser($proxy, $sessionId, $userId){
    $res = $proxy.GetUserById($sessionId, $userId)
    if($res.IsSuccesfull){
        return $res.UserData
    } else{
        Write-Host "Failed to Get Users : " $res.ErrorMessage
        exit 1
    }
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

$userId = getUserIdByEmail $proxy $sessionId $userEmail
$user = getUser $proxy $sessionId $userId

$proxyType = $proxy.gettype().Namespace

$userData = new-object ("$proxyType.UserData")

$teamId = getTeamId $proxy $sessionId $newTeamPath
$team = new-object ("$proxyType.Group")
$team.Guid = $teamId

$user.GroupList += $team

$userData.GroupList = $user.GroupList
$userData.RoleData = $user.RoleData
$userData.FirstName = $user.FirstName
$userData.LastName = $user.LastName
$userData.AuditUser = $user.AuditUser
$userData.IsActive = $user.IsActive
$userData.JobTitle = $user.JobTitle
$userData.CellPhone = $user.CellPhone
$userData.Phone = $user.Phone
$userData.AllowedIPs = $user.AllowedIPs
$userData.LimitAccessByIPAddress = $user.LimitAccessByIPAddress
$userData.UserPreferedLanguageLCID = $user.UserPreferedLanguageLCID
$userData.UserName = $user.Email
$userData.Password = $user.Password
$userData.Email = $userData.UserName
$userData.willExpireAfterDays = $user.willExpireAfterDays
$userData.Skype = $user.Skype

$userDeleted = deleteUserById $proxy $sessionId $userId

$res = $proxy.AddNewUser($sessionId, $userData, $userType)
if($res.IsSuccesfull){
    Write-Host "User ${userEmail} Updated with Success!"
} else{
    Write-Error "Failed to Add New User" $res.ErrorMessage
    Write-Error "User with ${email} might already exist"
}