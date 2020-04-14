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
######## Get Comments for a result ########
# Remark - Get Comments History All
# Severity - Get Number of Comments related with Severity Changes
# State - Get Number of Comments related with State Changes
# Assign - Get Number of Comments related with Assign Changes
# IssueTracking - Get Number of Comments related with IssueTracking Changes
# IgnorePath - Unknown
function getComments($proxy, $session, $scanId, $pathId){
    $res = $proxy.GetPathCommentsHistory($session, $scanId, $pathId, "Remark")
    if($res.IsSuccesfull){
        if($res.Path -and $res.Path.Comment){
            $commentArray = @($res.Path.Comment.Split("ÿ"))
            return $commentArray
        } else {
            return @()
        }
    } else {
        Write-Host "Failed to get Comment History for Scan ID ${scanId} and Path ID ${pathId}: " $res.ErrorMessage
        exit 5
    }
}
######## Get Result Description ########
function getResultDescription($proxy, $session, $scanId, $pathId){
    $res = $proxy.GetResultDescription($session, $scanId, $pathId)
    if($res.IsSuccesfull){
        $rawResultDescription = $res.ResultDescription

        $resultDescription = $rawResultDescription -replace "(<style>.*<\/style>)", ""
        $resultDescription = $resultDescription -replace "(<div>)", ""
        $resultDescription = $resultDescription -replace "(<\/div>)", ""
        $resultDescription = $resultDescription -replace "(<span[^>]*>)", ""
        $resultDescription = $resultDescription -replace "(<\/span>)", ""
        $resultDescription = $resultDescription -replace "(&quot;)", ""
        $resultDescription = $resultDescription -replace "(&nbsp;)", " "
        $resultDescription = $resultDescription -replace "(&#160;)", ""
        $resultDescription = $resultDescription -replace "(\\n)", ""
        $resultDescription = $resultDescription -replace "(<\/p>)", ""
        return $resultDescription
    } else {
        Write-Host "Failed to get Comment History for Scan ID ${scanId} and Path ID ${pathId}: " $res.ErrorMessage
        exit 5
    }
}
######## Get Query Description ########
function getQueryDescription($proxy, $session, $queryId){
    $res = $proxy.GetQueryDescriptionByQueryId($session, $queryId)
    if($res.IsSuccesfull){
        return $res.QueryDescription
    } else {
        Write-Host "Failed to get Query Description ${queryId}: " $res.ErrorMessage
        exit 5
    }
}
######## Get Queries For Scan ########
function getQueriesForScan($proxy, $session, $scanId){
    $res = $proxy.GetQueriesForScan($session, $scanId)
    if($res.IsSuccesfull){
        return $res.Queries
    } else {
        Write-Host "Failed to get Queries for Scan ${scanId}: " $res.ErrorMessage
        exit 5
    }
}
######## Get Result Path ########
function getResultPath($proxy, $session, $scanId, $pathId){
    $res = $proxy.GetResultPath($session, $scanId, $pathId)
    if($res.IsSuccesfull){
        return $res.Path
    } else {
        Write-Host "Failed to get Queries for Scan ${scanId}: " $res.ErrorMessage
        exit 5
    }
}
######## Get Query Details By Query ID ########
function getQueryDetailsByQueryId($queries, $queryId){
    foreach($query in $queries){
        if($query.QueryId -eq $queryId){
            return $query
        }
    }
    return null
}

$proxy = getProxy $domain

Write-Host "1 - Login into the Servers"
$session = login $proxy $username $password

Write-Host "2 - Get Project ${projectId}"
$projectLastScan = getProject $proxy $session $projectId
$lastScanId = $projectLastScan.ScanID

Write-Host "3 - Get Results for Project ${projectId} Last Scan ${lastScanId}"
$results = getResults $proxy $session $lastScanId

Write-Host "4 - Get Queries for Project ${projectId} Last Scan ${lastScanId}"
$queries = getQueriesForScan $proxy $session $lastScanId

Write-Host "5 - Get Comments for Results in Project ${projectId} Last Scan ${lastScanId}"
$totalResults = $results.Length
for($i=0; $i -lt $totalResults; $i++){
    $pathId = $results[$i].PathId
    $queryId = $results[$i].QueryId
    $percentage = [math]::Round((($i/$totalResults)*100), 0)
    if($percentage % 5 -eq 0){
        Write-Host "`t4.${i} - Get Comments/Nodes/Descriptions for Result ${pathId} in Project ${projectId} Last Scan ${lastScanId}...${i} out of ${totalResults} (${percentage} %)"
    }
    
    $query = getQueryDetailsByQueryId $queries $queryId
    Add-Member -InputObject $results[$i] -MemberType NoteProperty -Name Query -Value $query

    $queryDescription = getQueryDescription $proxy $session $queryId
    Add-Member -InputObject $results[$i] -MemberType NoteProperty -Name QueryDescription -Value $queryDescription
    
    $description = getResultDescription $proxy $session $lastScanId $pathId
    Add-Member -InputObject $results[$i] -MemberType NoteProperty -Name Description -Value $description

    $path = getResultPath $proxy $session $lastScanId $pathId
    Add-Member -InputObject $results[$i] -MemberType NoteProperty -Name SimilarityId -Value $path.SimilarityId
    Add-Member -InputObject $results[$i] -MemberType NoteProperty -Name Nodes -Value $path.Nodes

    $commentArray = getComments $proxy $session $lastScanId $pathId
    $results[$i].Comment = $commentArray
}
Write-Host ($results | ConvertTo-Json -Depth 99)
