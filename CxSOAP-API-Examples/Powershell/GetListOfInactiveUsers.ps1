######## Checkmarx Config ########
#Install-Module -Name "CredentialManager"
$credentials = Get-StoredCredential -Target "CxPortal" –AsCredentialObject
 
$domain = "http://localhost"
$username = $credentials.UserName
$password = $credentials.Password
$monthsAgo = 6

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
######## Get Percentage of Progress ########
function getPercentage($part, $total) {
    return [math]::Round((($part * 100) / $total), 2)
}

$proxy = getProxy $domain
$sessionId = login $proxy $username $password
$users = getUsers $proxy $sessionId

$totalUsers = $users.Count

Write-Host "Total Users: ${totalUsers}"

$activeUsersLessMonths = @()
$activeUsersMoreMonths = @()
$inactiveUsersMoreMonths = @()

foreach ($user in $users) {
    $id = $user.ID
    [datetime]$createdDate = $user.DateCreated
    [datetime]$lastLoginDate = $user.LastLoginDate
    if ((Get-Date).AddMonths(-$monthsAgo) -lt $createdDate) {
        $activeUsersLessMonths += $user
        # Users Created Less than X months ago
        # Write-Host "User ${id} Created at: ${createdDate} Last Login at: ${lastLoginDate}"
    }
    else {
        if ((Get-Date).AddMonths(-$monthsAgo) -lt $lastLoginDate) {
            $activeUsersMoreMonths += $user
            # Users Created More than X months ago but they logged in less than X months ago
            # Write-Host "User ${id} Created at: ${createdDate} Last Login at: ${lastLoginDate}"
        }
        else {
            $inactiveUsersMoreMonths += $user
            # Write-Host "User ${id} Created at: ${createdDate} Last Login at: ${lastLoginDate}"
        }
    }
}


$totalActiveLessMonths = $activeUsersLessMonths.Count
$totalActiveMoreMonths = $activeUsersMoreMonths.Count
$totalInactiveMoreMonths = $inactiveUsersMoreMonths.Count

Write-Host "Active Users (Less ${monthsAgo} months account created): ${totalActiveLessMonths} ("(getPercentage $totalActiveLessMonths $totalUsers )"%)"
Write-Host "Active Users (More ${monthsAgo} months account created): ${totalActiveMoreMonths} ("(getPercentage $totalActiveMoreMonths $totalUsers )"%)"
Write-Host "Inactive Users (More ${monthsAgo} months account created): ${totalInactiveMoreMonths} ("(getPercentage $totalInactiveMoreMonths $totalUsers )"%)`n`n"

foreach ($activeUserMoreMonths in $activeUsersMoreMonths) {
    $id = $activeUserMoreMonths.ID
    $email = $activeUserMoreMonths.Email
    $role = $activeUserMoreMonths.RoleData.Name
    [datetime]$lastLogin = $activeUserMoreMonths.LastLoginDate
    if (!($email -like "*@checkmarx.com") -and ($email -ne "admin@cx")) {
        #Write-Host "ACTIVE MORE ${monthsAgo} MONTHS - User ${id} - ${email} - ${role} - Last Login : ${lastLogin}"
    }
}

foreach ($inactiveUser in $inactiveUsersMoreMonths) {
    $id = $inactiveUser.ID
    $email = $inactiveUser.Email
    $role = $inactiveUser.RoleData.Name
    [datetime]$lastLogin = $inactiveUser.LastLoginDate
    if (!($email -like "*@checkmarx.com") -and ($email -ne "admin@cx")) {
        Write-Host "INACTIVE - User ${id} - ${email} - ${role} - Last Login : ${lastLogin}"
    }
}