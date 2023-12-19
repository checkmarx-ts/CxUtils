$startTime = get-date
Write-Host "`nStart: ${startTime}"
######## Source Checkmarx Config ########
#Install-Module -Name "CredentialManager"
#$credentialsSource = Get-StoredCredential -Target "CxPortal" –AsCredentialObject
   
$domainSource = "https://<Source URL>"
$usernameSource = "username or $credentialsSource.username"
$passwordSource = "passowrd or $credentialsSource.password"
$projectIdSourceArray = @(18, 21, 243)
  
######## Dest Checkmarx Config ########
#$credentialsDest = Get-StoredCredential -Target "CxTest" –AsCredentialObject
  
$domainDest = "https://<Destination URL>"
$usernameDest = "username or $credentialsDest.username"
$passwordDest = "password of $credentialsDest.password" 
$projectIdDestArray = @(4, 56, 90)
  
######## What to Update ? - Config ########
 
$updateComments = $true
$updateSeverity = $true
$updateState = $true
$updateAssignee = $true
 
######## Results Update Rate - Config ########
$resultsProcessPrintRate = 5 #Print Every 5% the Progress of comparing results
$resultsUpdateRate = 100 #Update 100 Results at Once
 
################ DO NOT EDIT THE CODE BELOW ################
$contentType = "text/xml; charset=utf-8"
$openSoapEnvelope = '<?xml version="1.0" encoding="utf-8"?><soap:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/"><soap:Body>'
$closeSoapEnvelope = '</soap:Body></soap:Envelope>'
$actionPrefix = 'http://Checkmarx.com'

######## Get URL ########
function getUrl($server){
    return "${server}/CxWebInterface/Portal/CxWebService.asmx"
}
######## Get Proxy ########
function getProxy($url){
	[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12
    return New-WebServiceProxy -Uri "${url}?wsdl"
}
######## Login ########
function getToken($server, $username, $password){
    $body = @{
        username = $username
        password = $password
        grant_type = "password"
        scope = "offline_access sast_api"
        client_id = "resource_owner_sast_client"
        client_secret = "014DF517-39D1-4453-B7B3-9930C563627C"
    }
    
    try {
        $response = Invoke-RestMethod -uri "${server}/cxrestapi/auth/identity/connect/token" -method post -body $body -contenttype 'application/x-www-form-urlencoded'
    } catch {
        Write-Host "StatusCode:" $_.Exception.Response.StatusCode.value__
        Write-Host "StatusDescription:" $_.Exception.Response.StatusDescription
        $result = $_.Exception.Response.GetResponseStream()
        $reader = New-Object System.IO.StreamReader($result)
        $reader.BaseStream.Position = 0
        $reader.DiscardBufferedData()
        $responseBody = $reader.ReadToEnd()
        Write-Host $responseBody
        throw "Could not authenticate - User: ${username}"
    }
    
    return $response.token_type + " " + $response.access_token
}
######## Get Headers ########
function getHeaders($token, $action){
    return @{
        Authorization = $token
        "SOAPAction" = "${actionPrefix}/${action}"
        "Content-Type" = $contentType
    }
}
######## Get Projects with Scans - Last Scan ########
function getLastScan($url, $token, $projectId){

    $payload = $openSoapEnvelope +'<GetScansDisplayData xmlns="http://Checkmarx.com">
                      <sessionID></sessionID>
                      <projectID>' + $projectId + '</projectID>
                    </GetScansDisplayData>' + $closeSoapEnvelope

    $headers = getHeaders $token "GetScansDisplayData"
    
    [xml]$res = (Invoke-WebRequest $url -Method POST -Body $payload -Headers $headers)
    
    $res1 = $res.Envelope.Body.GetScansDisplayDataResponse.GetScansDisplayDataResult

    if($res1.IsSuccesfull -and $res1.ScanList.ScanDisplayData.ChildNodes.Count -gt 0){
        if(-not $res1.ScanList.ScanDisplayData[0]){
            return $res1.ScanList.ScanDisplayData
        } else {
            return $res1.ScanList.ScanDisplayData[0]
        }
    } else {
        Write-Host "Failed to get Projects: " $res1.ErrorMessage
        Write-Host ($res1| ConvertTo-Json)
        exit 2
    }
}
######## Get Results for a Scan ########
function getResults($url, $token, $scanId){

    $payload = $openSoapEnvelope +'<GetResultsForScan xmlns="http://Checkmarx.com">
                      <sessionID></sessionID>
                      <scanId>' + $scanId + '</scanId>
                    </GetResultsForScan>' + $closeSoapEnvelope

    $headers = getHeaders $token "GetResultsForScan"
    
    [xml]$res = (Invoke-WebRequest $url -Method POST -Body $payload -Headers $headers)
    
    $res1 = $res.Envelope.Body.GetResultsForScanResponse.GetResultsForScanResult

    if($res1.IsSuccesfull){
        return $res1.Results.ChildNodes
    } 
    else {
        Write-Host "Failed to get Results: " $res1.ErrorMessage
        exit 4
    }
}
######## Get Queries for a Scan ########
function getQueries($url, $token, $scanId){

    $payload = $openSoapEnvelope +'<GetQueriesForScan xmlns="http://Checkmarx.com">
                      <sessionID></sessionID>
                      <scanId>' + $scanId + '</scanId>
                    </GetQueriesForScan>' + $closeSoapEnvelope

    $headers = getHeaders $token "GetQueriesForScan"
    
    [xml]$res = (Invoke-WebRequest $url -Method POST -Body $payload -Headers $headers)
    
    $res1 = $res.Envelope.Body.GetQueriesForScanResponse.GetQueriesForScanResult

    if($res1.IsSuccesfull){
        return $res1.Queries.ChildNodes
    } 
    else {
        Write-Host "Failed to get Queries for Scan ID ${scanId}:" $res1.ErrorMessage
        exit 4
    }
}
######## Get Comments for a result ########
function getComments($url, $token, $scanId, $pathId){
    $payload = $openSoapEnvelope +'<GetPathCommentsHistory xmlns="http://Checkmarx.com">
                      <sessionId></sessionId>
                      <scanId>' + $scanId + '</scanId>
                      <pathId>' + $pathId + '</pathId>
                      <labelType>Remark</labelType>
                    </GetPathCommentsHistory>' + $closeSoapEnvelope
    $headers = getHeaders $token "GetPathCommentsHistory"
    
    [xml]$res = (Invoke-WebRequest $url -Method POST -Body $payload -Headers $headers)
    
    $res1 = $res.Envelope.Body.GetPathCommentsHistoryResponse.GetPathCommentsHistoryResult

    if($res1.IsSuccesfull){
        return $res1.Path
    } 
    else {
        Write-Host "Failed to get Results Comments: " $res.ErrorMessage
        exit 5
    }
}
######## Get Query From List by ID ########
function getQuery($queryList, $queryId){
    for($i=0; $i -lt $queryList.Length; $i++){
        $q = $queryList[$i]
        if($q.QueryId -eq $queryId){
            return $q
        }
    }
    throw "Unable to get Query ${queryId}"
}
######## Check Queries are the same ########
function isEqualQuery($queriesSource, $queriesDest, $queryIdSource, $queryIdDest){

    $sourceQuery = getQuery $queriesSource $queryIdSource
    $destQuery = getQuery $queriesDest $queryIdDest

    return $sourceQuery.LanguageName -eq $destQuery.LanguageName -and $sourceQuery.QueryName -eq $destQuery.QueryName
}
######## Remove Accents From Strings ########
function RemoveDiacritics([System.String] $text){
    $regex = "[^a-zA-Z0-9='|/!(){}\s:-_;,]"
    if ([System.String]::IsNullOrEmpty($text)){
        return $text -replace $regex, "_"
    }
    $normalized = $text.Normalize([System.Text.NormalizationForm]::FormD)
    $newString = New-Object -TypeName System.Text.StringBuilder

    $normalized.ToCharArray() | ForEach{
        if ([Globalization.CharUnicodeInfo]::GetUnicodeCategory($psitem) -ne [Globalization.UnicodeCategory]::NonSpacingMark)
        {
            [void]$newString.Append($psitem)
        }
    }
    return $newString.ToString() -replace $regex, "_"
}
######## Get Results to Update ########
function getResultsToUpdate($urlSource, $namespace, $tokenSource, $tokenDest, $projectSource, $projectDest, $resultsSource, $resultsDest, $queriesSource, $queriesDest, $updateComments, $updateSeverity, $updateState, $updateAssignee){
      
    $rsdList = New-Object System.Collections.ArrayList
    $resultsCount = $resultsSource.Length
    For ($i=0; $i -lt $resultsSource.Length; $i++){
        $resultsPercentage = [math]::Round(($i*100.00)/$resultsCount, 0)
        if(($resultsPercentage % $resultsProcessPrintRate) -eq 0){
            Write-Host "`t5.${i} - Processing Results...(${i}/${resultsCount}) ${resultsPercentage}%"
        }
        $s = $resultsSource[$i]
        For ($j=0; $j -lt $resultsDest.Length; $j++){
            $d = $resultsDest[$j]
            if($s.DestFile.ToLower() -eq $d.DestFile.ToLower() -and $s.DestLine -eq $d.DestLine -and $s.DestObject.ToLower() -eq $d.DestObject.ToLower() -and
            $s.SourceFile.ToLower() -eq $d.SourceFile.ToLower() -and $s.SourceLine -eq $d.SourceLine -and $s.SourceObject.ToLower() -eq $d.SourceObject.ToLower() -and
            $s.NumberOfNodes -eq $d.NumberOfNodes -and $s.Comment.Length -gt 0){
                $queriesAreEqual = isEqualQuery $queriesSource $queriesDest $s.QueryId $d.QueryId
                if($queriesAreEqual){
                    if($updateComments){#Comments
                        Write-Host "`t5.${i}.${j} - Getting Comments from Source"
                        $commentsResp = getComments $urlSource $tokenSource $projectSource.ScanID $s.PathId
                        $comments = $commentsResp.Comment
                        $comments = $comments.Split("ÿ")
                        if($comments.Count -eq 1){
                            $comments = $comments.Replace(' ??', "ÿ").Split("ÿ")
                        }
                        foreach($comment in $comments){
                            if($comment.Length -gt 0){
                                $rsd = New-Object("$namespace.ResultStateData")
                                $rsd.ResultLabelType = 1
                                $rsd.projectId = $projectDest.ProjectId
                                $rsd.scanId = $projectDest.ScanID
                                $rsd.PathId = $d.PathId
                                $rsd.Remarks = RemoveDiacritics $comment
                                $rsd.data = RemoveDiacritics $comment
                                $rsdList.Add($rsd) | Out-Null
                            }
                        }
                    }
                
                    if($updateSeverity -and ($s.Severity -ne $d.Severity)){#Severity
                        Write-Host "`t5.${i}.${j} - Getting Severity from Source"
                        $rsdg = New-Object("$namespace.ResultStateData")
                        $rsdg.projectId = $projectDest.ProjectId
                        $rsdg.scanId = $projectDest.ScanID
                        $rsdg.PathId = $d.PathId
                        $rsdg.ResultLabelType = 2
                        $rsdg.data = $s.Severity
                        $rsdList.Add($rsdg) | Out-Null
                    }
                
                    if($updateState -and ($s.State -ne $d.State)){#Result State
                        Write-Host "`t5.${i}.${j} - Getting Result State from Source"
                        $rsdg = New-Object("$namespace.ResultStateData")
                        $rsdg.projectId = $projectDest.ProjectId
                        $rsdg.scanId = $projectDest.ScanID
                        $rsdg.PathId = $d.PathId
                        $rsdg.ResultLabelType = 3
                        $rsdg.data = $s.State
                        $rsdList.Add($rsdg) | Out-Null
                    }
                
                    if($updateAssignee -and ($s.AssignedUser -ne $d.AssignedUser)){#assignee
                        Write-Host "`t5.${i}.${j} - Getting Assignee from Source"
                        $rsdg = New-Object("$namespace.ResultStateData")
                        $rsdg.projectId = $projectDest.ProjectId
                        $rsdg.scanId = $projectDest.ScanID
                        $rsdg.PathId = $d.PathId
                        $rsdg.ResultLabelType = 4
                        $rsdg.data = $s.AssignedUser
                        $rsdList.Add($rsdg) | Out-Null
                    }
                } else {
                    Write-Host "`t5.${i}.${j} - Queries are not the same - Query ID Source:" $s.QueryId "- Query ID Dest:" $d.QueryId
                }
            }
        }
    }
    return $rsdList
}
######## Update Results ########
function updateResults($url, $token, $list, $listLength, $count){
    $listXml = ""
    For ($i=0; $i -lt $list.Length; $i++){
      $item = $list[$i]
      $scanId = $item.scanId
      $pathId = $item.PathId
      $resultLabelType = $item.ResultLabelType
      if($item.data){
        $data = $item.data.Replace("<", "").Replace(">", "")
      } else {
        $data = ""
      }
      $projectId = $item.projectId
      if($item.Remarks){
        $remarks = $item.Remarks.Replace("<", "").Replace(">", "")
      }
      else{
        $remarks= ""
      }
      $listXml += "<ResultStateData><scanId>${scanId}</scanId><PathId>${pathId}</PathId><projectId>${projectId}</projectId><Remarks>${remarks}</Remarks><ResultLabelType>${resultLabelType}</ResultLabelType><data>${data}</data></ResultStateData>"
    }

    $payload = $openSoapEnvelope +'<UpdateSetOfResultState xmlns="http://Checkmarx.com">
                      <sessionID></sessionID>
                      <resultsStates>' + $listXml + '</resultsStates>
                    </UpdateSetOfResultState>' + $closeSoapEnvelope

    $headers = getHeaders $token "UpdateSetOfResultState"
    
    [xml]$res = (Invoke-WebRequest $url -Method POST -Body $payload -Headers $headers)
    
    $res1 = $res.Envelope.Body.UpdateSetOfResultStateResponse.UpdateSetOfResultStateResult

    if($res1.IsSuccesfull){
        $percentage = [math]::Round($count*100.00/$listLength,2)
        Write-Host "`t5.1.1 - Updated ${percentage}% (${count}/${listLength})"
    } 
    else {
        Write-Host "`t5.1.1 - Error Updating : " $res1.ErrorMessage
        exit 5
    }
}

function updateData ($updateComments, $updateSeverity, $updateState, $updateAssignee) {
	
	Write-Host "5 - Comparing Results"
	$list = getResultsToUpdate $urlSource $namespace $tokenSource $tokenDest $projectLastScanSource $projectLastScanDest $resultsSource $resultsDest $queriesSource $queriesDest $updateComments $updateSeverity $updateState $updateAssignee

	Write-Host "6 - Total Updates Required: " $list.Length
	if($list.Length -ne 0){
		Write-Host "`t6.1 - Updating..."
		$smallList = @()
		$count = 0
		$listLength = $list.Length
		foreach($elem in $list){
			$smallList += $elem
			if($smallList.Length -eq $resultsUpdateRate){
				$count += $resultsUpdateRate
				updateResults $urlDest $tokenDest $smallList $listLength $count
				$smallList = @()
			}
		}
		if($smallList.Length -gt 0){
			$count += $smallList.Length
			updateResults $urlDest $tokenDest $smallList $listLength $count
			$smallList = @()
		}
	} else {
		Write-Host "7 - Nothing to Update"
	}
}


$urlSource = getUrl $domainSource
$urlDest = getUrl $domainDest

$proxy = getProxy $urlDest
$namespace = $proxy.gettype().Namespace

Write-Host "1 - Login into the Servers"
Write-Host "`t1.1 - Login into the Source Server - ${domainSource}"
$tokenSource = getToken $domainSource $usernameSource $passwordSource

Write-Host "`t1.2 - Login into the Dest Server - ${domainDest}"
$tokenDest = getToken $domainDest $usernameDest $passwordDest
  
if($projectIdSourceArray.Length -eq $projectIdDestArray.Length){
    Write-Host "`nProjects to Update: " $projectIdDestArray.Length
    For ($i=0; $i -lt $projectIdSourceArray.Length; $i++) {
        $startTimeProject = get-date
        $projectIdSource = $projectIdSourceArray[$i];
        $projectIdDest = $projectIdDestArray[$i];
        Write-Host "`nProject ${projectIdDest} - Process Start: ${startTimeProject}"
        Write-Host "Migrating : Source Project " $projectIdSource " to Dest Project "$projectIdDest
  
        Write-Host "2 - Get Project Info"
        $projectLastScanSource = getLastScan $urlSource $tokenSource $projectIdSource
        $projectNameSource = $projectLastScanSource.ProjectName
        Write-Host "`t2.1 - Get Project Info Source - " $projectIdSource $projectNameSource
        $projectLastScanDest = getLastScan $urlDest $tokenDest $projectIdDest
        $projectNameDest = $projectLastScanDest.ProjectName
        Write-Host "`t2.2 - Get Project Info Dest - " $projectIdDest $projectNameDest
        
        $locSource = $projectLastScanSource.LOC
        $locDest = $projectLastScanDest.LOC
        if ($locSource -ne $locDest){
            $diffLoc = Read-Host "LOC (${locSource}) from Source is different from LOC (${locDest}) Destination. Do you want to proceed ? (y/n)"
            if($diffLoc -ne "y"){
                continue
            }
        }

        $highSource = $projectLastScanSource.HighSeverityResults
        $mediumSource = $projectLastScanSource.MediumSeverityResults
        $lowSource = $projectLastScanSource.LowSeverityResults
        $totalSource = $highSource + $mediumSource + $lowSource
        
        $highDest = $projectLastScanDest.HighSeverityResults
        $mediumDest = $projectLastScanDest.MediumSeverityResults
        $lowDest = $projectLastScanDest.LowSeverityResults
        $totalDest = $highDest + $mediumDest + $lowDest
        if (($highSource -ne $highDest) -or ($mediumSource -ne $mediumDest) -or ($lowSource -ne $lowDest)){
            $diffResults = Read-Host "Results Total(${totalSource}), High(${highSource}), Medium(${mediumSource}), Low(${lowSource}) from Source is different from Results Total(${totalDest}), High(${highDest}), Medium(${mediumDest}), Low(${lowDest}) Destination. Do you want to proceed ? (y/n)"
            if($diffResults -ne "y"){
                continue
            }
        }

        $scanVersionSource = $projectLastScanSource.CxVersion
        $scanVersionDest = $projectLastScanDest.CxVersion
          
        if($scanVersionSource -eq $scanVersionDest){
            $list = @()
 
            Write-Host "3 - Get Results for the Scans"
            Write-Host "`t3.1 - ScanID SRC:" $projectLastScanSource.ScanID
            Write-Host "`t3.2 - ScanID DEST:" $projectLastScanDest.ScanID
            $resultsSource = getResults $urlSource $tokenSource $projectLastScanSource.ScanID
            Write-Host "`t3.3 - Get Results for the Scans Source:" $resultsSource.Count
            $resultsDest = getResults $urlDest $tokenDest $projectLastScanDest.ScanID
            Write-Host "`t3.4 - Get Results for the Scans Dest:" $resultsDest.Count
            if ($resultsSource.Count -ne $resultsDest.Count){
                $diff = Read-Host "Results from Source are different from Destination. Do you want to proceed ? (y/n)"
                if($diff -ne "y"){
                    continue
                }
            }

            Write-Host "4 - Get Queries for the Scans"
            $queriesSource = getQueries $urlSource $tokenSource $projectLastScanSource.ScanID
            Write-Host "`t4.1 - Get Queries for the Scans Source ID" $projectLastScanSource.ScanID ":" $queriesSource.Count
            $queriesDest = getQueries $urlDest $tokenDest $projectLastScanDest.ScanID
            Write-Host "`t4.1 - Get Queries for the Scans Dest ID" $projectLastScanDest.ScanID ":" $queriesDest.Count

			# Update comments
			updateData $true $false $false $false
			# Update severity
			updateData $false $true $false $false
			# Update state
			updateData $false $false $true $false
			# Update assignee
			updateData $false $false $false $true
			
        } else {
            Write-Host "Different Versions of Scans - Source: " $scanVersionSource " Dest: " $scanVersionDest
        }
        $endTimeProject = get-date
        $durationProject = New-TimeSpan -Start $startTimeProject -End $endTimeProject
        Write-Host "Project ${projectIdDest} - ${projectNameDest} End: ${endTimeProject}"
        Write-Host "Project ${projectIdDest} - ${projectNameDest} Duration: ${durationProject}"
    }
} else {
    Write-Host "Array of Projects IDs in the Source different of Array of Projects IDs in the Dest: " $projectIdSourceArray.Length " != " $projectIdDestArray.Length
}
$endTime = get-date
$nts = New-TimeSpan -Start $startTime -End $endTime
Write-Host "`nStart: ${startTime}"
Write-Host "End: ${endTime}"
Write-Host "Total Duration: ${nts}"