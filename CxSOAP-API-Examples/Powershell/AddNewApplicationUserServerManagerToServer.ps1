######## Checkmarx Config ########
#Install-Module -Name "CredentialManager"
$credentials = Get-StoredCredential -Target "CxPortal" –AsCredentialObject
 
$domain = "http://localhost"
$username = $credentials.UserName
$password = $credentials.Password

# Available Roles IDs:
# 0 - Scanner
# 1/3 - Reviewer
# 2 - Company Manager
# 4 - SP Manager
# 5 - Server Manager
[int]$roleId = 5
# Available Languages:
# 1028 - Chinese_Taiwan           
# 1033 - English                  
# 1034 - Spanish                  
# 1036 - French                   
# 1041 - Japanese                 
# 1042 - Korean                   
# 1046 - Portuguese               
# 1049 - Russian                  
# 2052 - Chinese                  
$lcid = 1033
# Available User Types:
# Application
# Domain
# OpenID
# SAML
# SSO
# LDAP
# None
$userType = "Application"

$firstName = "Server"
$lastName = "Manager"
$email = "server.manager@cx"
$password = "Admin123."
$isAuditor = $false
$isActive = $true
$jobTitle = "Server Manager"
$cellPhone = "999999999"
$phone = "999999999"
$allowedIps = @()
$limitIpAccess = $false
$expireDays = 14
$skype = "mySkypeUser"

$teamPath = "/CxServer" # Existing Team Path - Server Level

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
######## Get Team Full Path ########
function getTeamFullPath($proxy, $sessionId, $teamId){
    $res = $proxy.GetTeamFullPaths($sessionId, $teamId, $teamId)
    return $res.sourceTeamFullPath
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
function getCRUDAction($proxyType, $type, [bool]$isEnabled){
    $crudAction = new-object ("$proxyType.CxWSEnableCRUDAction")
    $crudAction.Type = $type
    $crudAction.Enable = $isEnabled
    return $crudAction
}
function getItemsCRUD($proxyType, $type, [int]$roleId, [bool]$deleteProjectsScans, [bool]$proposeNotExpoitable, [bool]$changeSeverity){
    $crud = new-object ("$proxyType.CxWSItemAndCRUD")
    $crud.Type = $type

    if($roleId -eq 0){ # Scanner
        if(-not $deleteProjectsScans -and -not $proposeNotExpoitable){ # Scanner only
            if($type -eq "ResultStatus" -or $type -eq "ResultSeverity"){
                $create = getCRUDAction $proxyType "Create" $false
                $delete = getCRUDAction $proxyType "Delete" $false
                $update = getCRUDAction $proxyType "Update" $false
                $view = getCRUDAction $proxyType "View" $true
                $run = getCRUDAction $proxyType "Run" $false
                $investigate = getCRUDAction $proxyType "Investigate" $false
            }
            if($type -eq "Scan" -or $type -eq "Project"){
                $create = getCRUDAction $proxyType "Create" $true
                $delete = getCRUDAction $proxyType "Delete" $false
                $update = getCRUDAction $proxyType "Update" $true
                $view = getCRUDAction $proxyType "View" $true
                $run = getCRUDAction $proxyType "Run" $true
                $investigate = getCRUDAction $proxyType "Investigate" $false
            }
        }
        if(-not $deleteProjectsScans -and $proposeNotExpoitable){ # Scanner with Propose NE
            if($type -eq "ResultStatus" -or $type -eq "ResultSeverity"){
                $create = getCRUDAction $proxyType "Create" $false
                $delete = getCRUDAction $proxyType "Delete" $false
                $update = getCRUDAction $proxyType "Update" $true
                $view = getCRUDAction $proxyType "View" $true
                $run = getCRUDAction $proxyType "Run" $false
                $investigate = getCRUDAction $proxyType "Investigate" $false
            }
            if($type -eq "Scan" -or $type -eq "Project"){
                $create = getCRUDAction $proxyType "Create" $true
                $delete = getCRUDAction $proxyType "Delete" $false
                $update = getCRUDAction $proxyType "Update" $true
                $view = getCRUDAction $proxyType "View" $true
                $run = getCRUDAction $proxyType "Run" $true
                $investigate = getCRUDAction $proxyType "Investigate" $false
            }
        }
        if($deleteProjectsScans -and -not $proposeNotExpoitable){ # Scanner with Delete Projects/Scans
            if($type -eq "ResultStatus" -or $type -eq "ResultSeverity"){
                $create = getCRUDAction $proxyType "Create" $false
                $delete = getCRUDAction $proxyType "Delete" $false
                $update = getCRUDAction $proxyType "Update" $false
                $view = getCRUDAction $proxyType "View" $true
                $run = getCRUDAction $proxyType "Run" $false
                $investigate = getCRUDAction $proxyType "Investigate" $false
            }
            if($type -eq "Scan" -or $type -eq "Project"){
                $create = getCRUDAction $proxyType "Create" $true
                $delete = getCRUDAction $proxyType "Delete" $true
                $update = getCRUDAction $proxyType "Update" $true
                $view = getCRUDAction $proxyType "View" $true
                $run = getCRUDAction $proxyType "Run" $true
                $investigate = getCRUDAction $proxyType "Investigate" $false
            }
        }
        if($deleteProjectsScans -and $proposeNotExpoitable){ # Scanner with Delete Projects/Scans and Propose NE
            if($type -eq "ResultStatus" -or $type -eq "ResultSeverity"){
                $create = getCRUDAction $proxyType "Create" $false
                $delete = getCRUDAction $proxyType "Delete" $false
                $update = getCRUDAction $proxyType "Update" $true
                $view = getCRUDAction $proxyType "View" $true
                $run = getCRUDAction $proxyType "Run" $false
                $investigate = getCRUDAction $proxyType "Investigate" $false
            }
            if($type -eq "Scan" -or $type -eq "Project"){
                $create = getCRUDAction $proxyType "Create" $true
                $delete = getCRUDAction $proxyType "Delete" $true
                $update = getCRUDAction $proxyType "Update" $true
                $view = getCRUDAction $proxyType "View" $true
                $run = getCRUDAction $proxyType "Run" $true
                $investigate = getCRUDAction $proxyType "Investigate" $false
            }
        }
    }
    
    if($roleId -eq 1 -or $roleId -eq 3){ # Reviewer
        if(-not $changeSeverity){ # Reviewer only
            if($type -eq "ResultStatus" -or $type -eq "ResultSeverity"){
                $create = getCRUDAction $proxyType "Create" $false
                $delete = getCRUDAction $proxyType "Delete" $false
                $update = getCRUDAction $proxyType "Update" $false
                $view = getCRUDAction $proxyType "View" $true
                $run = getCRUDAction $proxyType "Run" $false
                $investigate = getCRUDAction $proxyType "Investigate" $false
            }
            if($type -eq "Scan" -or $type -eq "Project"){
                $create = getCRUDAction $proxyType "Create" $true
                $delete = getCRUDAction $proxyType "Delete" $false
                $update = getCRUDAction $proxyType "Update" $true
                $view = getCRUDAction $proxyType "View" $true
                $run = getCRUDAction $proxyType "Run" $true
                $investigate = getCRUDAction $proxyType "Investigate" $false
            }
        }
        if($changeSeverity){ # Reviewer with Severity
            if($type -eq "ResultStatus" -or $type -eq "ResultSeverity"){
                $create = getCRUDAction $proxyType "Create" $false
                $delete = getCRUDAction $proxyType "Delete" $false
                $update = getCRUDAction $proxyType "Update" $true
                $view = getCRUDAction $proxyType "View" $true
                $run = getCRUDAction $proxyType "Run" $false
                $investigate = getCRUDAction $proxyType "Investigate" $false
            }
            if($type -eq "Scan" -or $type -eq "Project"){
                $create = getCRUDAction $proxyType "Create" $true
                $delete = getCRUDAction $proxyType "Delete" $false
                $update = getCRUDAction $proxyType "Update" $true
                $view = getCRUDAction $proxyType "View" $true
                $run = getCRUDAction $proxyType "Run" $true
                $investigate = getCRUDAction $proxyType "Investigate" $false
            }
        }
    }
    if($roleId -eq 2){ # Company Manager
        if($type -eq "ResultStatus" -or $type -eq "ResultSeverity"){
            $create = getCRUDAction $proxyType "Create" $false
            $delete = getCRUDAction $proxyType "Delete" $false
            $update = getCRUDAction $proxyType "Update" $true
            $view = getCRUDAction $proxyType "View" $true
            $run = getCRUDAction $proxyType "Run" $false
            $investigate = getCRUDAction $proxyType "Investigate" $false
        }
        if($type -eq "Scan" -or $type -eq "Project"){
            $create = getCRUDAction $proxyType "Create" $true
            $delete = getCRUDAction $proxyType "Delete" $true
            $update = getCRUDAction $proxyType "Update" $true
            $view = getCRUDAction $proxyType "View" $true
            $run = getCRUDAction $proxyType "Run" $true
            $investigate = getCRUDAction $proxyType "Investigate" $false
        }
    }
    if($roleId -eq 4){ # SP Manager
        if($type -eq "ResultStatus" -or $type -eq "ResultSeverity"){
            $create = getCRUDAction $proxyType "Create" $false
            $delete = getCRUDAction $proxyType "Delete" $false
            $update = getCRUDAction $proxyType "Update" $true
            $view = getCRUDAction $proxyType "View" $true
            $run = getCRUDAction $proxyType "Run" $false
            $investigate = getCRUDAction $proxyType "Investigate" $false
        }
        if($type -eq "Scan" -or $type -eq "Project"){
            $create = getCRUDAction $proxyType "Create" $true
            $delete = getCRUDAction $proxyType "Delete" $true
            $update = getCRUDAction $proxyType "Update" $true
            $view = getCRUDAction $proxyType "View" $true
            $run = getCRUDAction $proxyType "Run" $true
            $investigate = getCRUDAction $proxyType "Investigate" $false
        }
    }
    if($roleId -eq 5){ # Server Manager
        if($type -eq "ResultStatus" -or $type -eq "ResultSeverity"){
            $create = getCRUDAction $proxyType "Create" $false
            $delete = getCRUDAction $proxyType "Delete" $false
            $update = getCRUDAction $proxyType "Update" $true
            $view = getCRUDAction $proxyType "View" $true
            $run = getCRUDAction $proxyType "Run" $false
            $investigate = getCRUDAction $proxyType "Investigate" $false
        }
        if($type -eq "Scan" -or $type -eq "Project"){
            $create = getCRUDAction $proxyType "Create" $true
            $delete = getCRUDAction $proxyType "Delete" $true
            $update = getCRUDAction $proxyType "Update" $true
            $view = getCRUDAction $proxyType "View" $true
            $run = getCRUDAction $proxyType "Run" $true
            $investigate = getCRUDAction $proxyType "Investigate" $false
        }
    }

    $crud.CRUDActionList = @(
        $create, 
        $delete,
        $update,
        $view,
        $run,
        $investigate
    )
    return $crud
}
function getServerManagerCRUD($proxyType){
    $crudArray = @()
    $types = @("ResultStatus", "ResultSeverity", "Scan", "Project")
    foreach($type in $types){
        $crud = getItemsCRUD $proxyType $type 5 $false $false $false
        $crudArray += $crud
    }
    return $crudArray
}

function getRoleData($proxyType, [int]$roleId){
    $roleData = new-object ("$proxyType.CxWSRoleWithUserPrivileges")
    $roleData.ID = $roleId
    $roleData.ItemsCRUD = getServerManagerCRUD $proxyType

    return $roleData
}

$proxy = getProxy $domain
$sessionId = login $proxy $username $password
$teamId = getTeamId $proxy $sessionId $teamPath

$proxyType = $proxy.gettype().Namespace

$userData = new-object ("$proxyType.UserData")

$team = new-object ("$proxyType.Group")
$team.Guid = $teamId

$userData.GroupList = @($team)
$roleData = getRoleData $proxyType $roleId

$userData.RoleData = $roleData
$userData.FirstName = $firstName
$userData.LastName = $lastName
$userData.AuditUser = $isAuditor
$userData.IsActive = $isActive
$userData.JobTitle = $jobTitle
$userData.CellPhone = $cellPhone
$userData.Phone = $phone
$userData.AllowedIPs = $allowedIps
$userData.LimitAccessByIPAddress = $limitIpAccess
$userData.UserPreferedLanguageLCID = $lcid
$userData.UserName = $email
$userData.Password = $password
$userData.Email = $userData.UserName
$userData.willExpireAfterDays = $expireDays
$userData.Skype = $skype

$res = $proxy.AddNewUser($sessionId, $userData, $userType)
if($res.IsSuccesfull){
    Write-Host "User Created with Success!"
} else{
    Write-Error "Failed to Add New User" $res.ErrorMessage
    Write-Error "User with ${email} might already exist"
}