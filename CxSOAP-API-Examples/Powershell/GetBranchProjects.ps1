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
######## Get Project Source Settings ########
function getProjectSourceSettings($proxy, $sessionId, $projectId){
    $res = $proxy.GetProjectConfiguration($sessionId, $projectId)
    if($res.IsSuccesfull){
        return $res.ProjectConfig.SourceCodeSettings
    } else {
        Write-Error "Failed to get project ${projectId} configuration" $res.ErrorMessage
    }
}
######## Get All Projects ########
function getProjects($proxy, $sessionId){
    $res = $proxy.GetProjectsDisplayData($sessionId)
    if($res.IsSuccesfull){
        return $res.projectList
    } else {
        Write-Error "Failed to get projects" $res.ErrorMessage
    }
}
######## Check if Project is a Branch ########
function isBranchProject($proxy, $sessionId, $projectId){
    $res = $proxy.GetProjectBranchingStatus($sessionId,$projectId) 
    if($res.IsSuccesfull){
        return $true
    } else {
        return $false
    }
}
######## Get Branch Projects ########
function getBranchProjects($proxy, $sessionId){
    $branchProjects = @()
    foreach($project in $projects){
        $projectId = $project.projectID
        $projectName = $project.projectName
        $res = $proxy.GetProjectBranchingStatus($sessionId,$projectId) 
        if($res.IsSuccesfull){
            $branchProject = @{
                projectId = $projectId
                projectName = $projectName
            }
            $branchProjects += $branchProject
        }
    }
    return $branchProjects
}
######## Get Branch Details ########
function getBranchDetails($proxy, $sessionId, $projects, $branch){
    $branchProjectId = $branch.projectId
    $branchProjectName = $branch.projectName
    $branchSourceSettings = getProjectSourceSettings $proxy $sessionId $projectId
    $branchRepoBranch = $branchSourceSettings.PathList.Path
    $branchRepoUrl = $branchSourceSettings.SourceControlSetting.ServerName
    foreach($project in $projects){
        $parentProjectId = $project.projectID
        $parentProjectName = $project.projectName
        $parentIsBranch = isBranchProject $proxy $sessionId $parentProjectId
        if(-not $parentIsBranch){
            $parentSourceSettings = getProjectSourceSettings $proxy $sessionId $parentProjectId
            $parentRepoUrl = $parentSourceSettings.SourceControlSetting.ServerName
            $parentRepoBranch = $branchSourceSettings.PathList.Path
            if($parentRepoUrl -eq $branchRepoUrl){
                $branchDetails = @{
                    branchProjectId = $branchProjectId
                    branchProjectName = $branchProjectName
                    branchRepoBranch = $branchRepoBranch
                    branchRepoUrl = $branchRepoUrl
                    parentProjectId = $parentProjectId
                    parentProjectName = $parentProjectName
                    parentRepoBranch = $parentRepoBranch
                    parentRepoUrl = $parentRepoUrl
                }
                return $branchDetails
            }
        }
    }

    Write-Error "Unable to find Branch Details for project ${branchProjectId} - ${branchProjectName}"
}

$proxy = getProxy $domain
$sessionId = login $proxy $username $password
$projects = getProjects $proxy $sessionId
$branchProjects = getBranchProjects $proxy $sessionId $projects

$branchProjectDetails = @()
foreach ($branchProject in $branchProjects){
    $branchProjectDetails += getBranchDetails $proxy $sessionId $projects $branchProject
}

($branchProjectDetails| ConvertTo-Json)