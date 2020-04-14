######## Source Checkmarx Config ########
#Install-Module -Name "CredentialManager"
$credentials = Get-StoredCredential -Target "CxPortal" –AsCredentialObject
 
$domain = "http://localhost"
$username = $credentials.UserName
$password = $credentials.Password
$projectId = 33 #Valid Project ID with Scans

################ DO NOT EDIT THE CODE BELOW ################
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
######## Get Projects with Scans ########
function getProject($proxy, $session, $projectId){
    $res = $proxy.GetScansDisplayData($session, $projectId)
    if($res.IsSuccesfull -and $res.ScanList.Count -gt 0){
        return $res.ScanList[0]
    } else{
        Write-Host "Failed to get Projects: " $res.ErrorMessage
        exit 2
    }
}
######## Get Results for a Scan ########
function getResults($proxy, $session, $scanId){
    $res = $proxy.GetResultsForScan($session, $scanId)
    if($res.IsSuccesfull){
        return $res.Results
    } else {
        Write-Host "Failed to get Results: " $res.ErrorMessage
        exit 3
    }
}

######## Update set of Results for a Scan ########
function updateResults($proxy, $session, $listOfResults){
    $res = $proxy.UpdateSetOfResultState($session, $listOfResults)
    if($res.IsSuccesfull){
        Write-Host "Results" $listOfResults.Length "updated!"
        return $true
    } else {
        Write-Host "Failed to update Results: " $res.ErrorMessage
        exit 4
    }
}

$proxy = getProxy $domain

Write-Host "1 - Login into the Servers"
$session = login $proxy $username $password

Write-Host "2 - Get Project ${projectId}"
$projectLastScan = getProject $proxy $session $projectId
$lastScanId = $projectLastScan.ScanID

Write-Host "3 - Get Results for Project ${projectId} Last Scan ${lastScanId}"
$results = getResults $proxy $session $lastScanId

##### CHANGE ME
# Remarks and data:
# Comment
$myComment = "my test comment"
$resultToUpdateState = @(@{
    projectId = $projectId
    scanId = $lastScanId
    PathId = $results[0].PathId
    ResultLabelType = 1 # Comments
    Remarks = $myComment
    data = $myComment
})

updateResults $proxy $session $resultToUpdateState

