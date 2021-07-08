# --------------------------------------------------------------------------------------------
#
# Utility to request list of Repos from Gitlab, Clone and then run a CLOC report 
# Write results of Repos that have Cx supported	languages to a CSV
# Use 'License Report.xlsx to view results and calculate no. of requires Cx Project licenses
#
# --------------------------------------------------------------------------------------------


$deleteReport = "true"

function scanGitlab
{
	$page = 1
	$rec = 1

	$token = Read-Host -Prompt 'Please enter your Gitlab personal token ---> '
	# We need to loop through results as the API only returns max 100 results
	# Increment page, to get next resutls. Set a limit though ....
	while($page -lt 101)
	{
		$URI = "https://gitlab.com/api/v4/projects?private_token=" + $token + "&visibility=private&simple=true&per_page=100&page=" + $page 
		Write-Output $URI
		$response = Invoke-WebRequest -Uri $URI -UseBasicParsing
		$myjson = $response | ConvertFrom-Json
		
		#Write the repo details to file for resilience in processing large numbers of them
		foreach ($repo in $myjson) {
			$out = $repo.name + "," + $repo.http_url_to_repo
			Write-Output $out | Out-File -FilePath .\initialRepoList.txt -Append
			Write-Output $out 
			$rec = $rec + 1
		}
		if ($rec -eq 101) # Only increment page if rec has not reached limit of 100
		{
			$page = $page + 1
		}
		else{
			break
		}
		# Reset counter
		$rec = 0
	}
}

function scanGitHub
{
	$page = 1
	$rec = 1
	$user = Read-Host -Prompt 'Please enter your GitHub Organisation name ---> '
	$token = Read-Host -Prompt 'Please enter your personal token ---> '
	# We need to loop through results as the API only returns max 100 results
	# Increment page, to get next resutls. Set a linmit though ....
	while($page -lt 6)
	{
	
		$URI = "https://api.github.com/orgs/" + $user + "/repos?access_token=" + $token + "&per_page=100&page=" + $page
		Write-Output $URI
		$response = Invoke-WebRequest -Uri $URI -UseBasicParsing
		$myjson = $response | ConvertFrom-Json
		
		#Write the repo details to file for resilience in processing large numbers of them
		foreach ($repo in $myjson) {
			$out = $repo.name + "," + $repo.clone_url
			Write-Output $out | Out-File -FilePath .\initialRepoList.txt -Append
			Write-Output $out 
			$rec = $rec + 1
		}
		if ($rec -eq 101) # Only increment page if rec has not reached limit of 100
		{
			$page = $page + 1
		}
		else{
			break
		}
		# Reset counter
		$rec = 0
	}
}

function scanBitBucket
{
	$page = 1
	$rec = 0
	$user = Read-Host -Prompt 'Please enter your BitBucket userid ---> '
	$token = Read-Host -Prompt 'Please enter your personal token ---> '

	$pair = "$($user):$($token)"
	$encodedCreds = [System.Convert]::ToBase64String([System.Text.Encoding]::ASCII.GetBytes($pair))
	$basicAuthValue = "Basic $encodedCreds"
	$Headers = @{
		Authorization = $basicAuthValue
	}


	
	# We need to loop through results as the API only returns max 100 results
	# Increment page, to get next resutls. Set a linmit though ....
	while($page -lt 6)
	{
	
		# https://api.bitbucket.org/2.0/repositories/andrew_thompson_cx?pagelen=10&fields=next,values.links.clone.href,values.name
		$URI = "https://api.bitbucket.org/2.0/repositories/" + $user + "?pagelen=100&fields=next,values.links.clone.href,values.name"
		Write-Output $URI
		$response = Invoke-WebRequest -Uri $URI -UseBasicParsing -Headers $Headers
		
		$myjson = $response.Content | ConvertFrom-Json
		
		Write-Output "Count " +  $myjson.values.name.Count
	
		#Write the repo details to file for resilience in processing large numbers of them
		for($i = 0; $i -lt $myjson.values.name.Count; $i++) {
		
			$out = $myjson.values.name[$i] + "," + $myjson.values.links[$i].clone.href[0]
			Write-Output $out | Out-File -FilePath .\initialRepoList.txt -Append
			$rec = $rec + 1
		}
		if ($rec -eq 101) # Only increment page if rec has not reached limit of 100
		{
			$page = $page + 1
		}
		else{
			break
		}
		# Reset counter
		$rec = 0
	}
}

function scanADO
{
	$page = 1
	$rec = 0
	$user = Read-Host -Prompt 'Please enter your ADO userid ---> '
	$token = Read-Host -Prompt 'Please enter your personal token ---> '
	$adoOrg = Read-Host -Prompt 'Please enter your ADO Organization ---> '

	$pair = ":$($token)"
	$encodedCreds = [System.Convert]::ToBase64String([System.Text.Encoding]::ASCII.GetBytes($pair))
	$basicAuthValue = "Basic $encodedCreds"
	$Headers = @{
		Authorization = $basicAuthValue
	}


	# We need to loop through results as the API only returns max 100 results
	# Increment page, to get next resutls. Set a linmit though ....
	while($page -lt 6)
	{
	
		$URI = "https://dev.azure.com/" + $adoOrg + "/_apis/git/repositories?api-version=5.1&includeAllUrls=true&includeHidden=true"
		Write-Output $URI
		$response = Invoke-WebRequest -Uri $URI -UseBasicParsing -Headers $Headers
		
		Write-Output $response
		
		$myjson = $response.Content | ConvertFrom-Json
			
		#Write the repo details to file for resilience in processing large numbers of them
		for($i = 0; $i -lt $myjson.value.name.Count; $i++) {
		
			$out = $myjson.value.name[$i] + "," + $myjson.value.webUrl[$i]
			Write-Output $out | Out-File -FilePath .\initialRepoList.txt -Append
			$rec = $rec + 1
		}
		if ($rec -eq 101) # Only increment page if rec has not reached limit of 100
		{
			$page = $page + 1
		}
		else{
			break
		}
		# Reset counter
		$rec = 0
	}
	
}


# ------------------------------------

# Check if the CLOC tool is installed.

# ------------------------------------

$fileToCheck = ".\cloc-1.86.exe"
if (Test-Path $fileToCheck -PathType leaf)
{
    Write-Output "CLOC tool found"
}
else
{
	$clocRequest = ""
	While ($clocRequest -ne "y")
	{
		Write-Output "CLOC tool is required, this is found here: https://github.com/AlDanial/cloc/releases/"
		$clocRequest = Read-Host -Prompt 'Press y to download via curl or, q to Quit if you want download to manually (place in same directory as this script)'
		if ($clocRequest -eq "y")
		{
			Write-Output "Downloading CLOC"
			curl https://github.com/AlDanial/cloc/releases/download/1.86/cloc-1.86.exe -o ./cloc-1.86.exe
		}
		else{
			if ($clocRequest -eq "q")
			{
				exit(1)
			}
		}
	}
}


# -----------------------------

# Delete working files

# -----------------------------
$fileToCheck = ".\unifiedClockReport.csv"
if (Test-Path $fileToCheck -PathType leaf)
{
    Remove-Item .\unifiedClockReport.csv
}

$fileToCheck = ".\ClockReportException.csv"
if (Test-Path $fileToCheck -PathType leaf)
{
    Remove-Item .\ClockReportException.csv
}


Remove-Item .\initialRepoList.txt

# -----------------------------

# Ask which repo to use

# -----------------------------

	$whichRepo = ""
	
	While ($whichRepo -eq "")
	{
		Write-Output "Which Repo do you want to Scan (Respond 1, 2, or q to quit"
		Write-Output "1/ GitLab"
		Write-Output "2/ GitHub"
		Write-Output "3/ BitBucket/Stash"
		Write-Output "4/ ADO"
		Write-Output "q - quit"
		$whichRepo = Read-Host -Prompt '---> '
		if ($whichRepo -eq "1")
		{
			Write-Output "Scanning GitLab"
			scanGitlab
		}
		elseif ($whichRepo -eq "2")
		{
			Write-Output "Scanning GitHub"
			scanGitHub
		}
		elseif ($whichRepo -eq "3")
		{
			Write-Output "Scanning BitBucket/Stash"
			scanBitBucket
		}
		elseif ($whichRepo -eq "4")
		{
			Write-Output "Scanning ADO"
			scanADO
			
		}
		else
		{
			if ($whichRepo -eq "q")
			{
				exit(1)
			}
			else 
			{	
				$whichRepo = ""
			}
		}
	}
	


# -----------------------------

#Read the repo report and extract project & url
$file = get-item .\initialRepoList.txt		
$repoStreamreader = New-Object -TypeName System.IO.StreamReader -ArgumentList $file	
while (($readeachrepo = $repoStreamreader.ReadLine()) -ne $null)
{
		$line = $readeachrepo.Split(",") 
		$name = $line[0]
		$repoURL = $line[1]

		Write-Output " Name is " $name  "URL is " $repoURL

		$LOC = 0
		$Languages = "" 
		$excludedLanguages = "" 


		# create Dir to put clone into
		mkdir  $name
		cd $name
		git clone $repoURL

		# Run CLOC against the cloned repo and pipe to a file
		..\cloc-1.86.exe . > ..\$name.log
		
		#Delete the repo dir as its no longer needed
		cd c:/cxgit
		Remove-Item .\$name -recurse -force
		
		#Read the CLOC report and extract languages and LOC
		$file = get-item .\$name.log		
		$clocStreamreader = New-Object -TypeName System.IO.StreamReader -ArgumentList $file
		$eachlinenumber = 1
				while (($readeachline = $clocStreamreader.ReadLine()) -ne $null)
		{
			$line = -split $readeachline 
			#Write-Output $line
			if ($line[0].Equals("Java") `
				-Or $line[0].Equals("Ruby") `
				-Or $line[0].Equals("Python") `
				-Or $line[0].Equals("JavaScript") `
				-Or $line[0].Equals("C#") `
				-Or $line[0].Equals("Ruby") `
				-Or $line[0].Equals("PHP") `
				-Or $line[0].Equals("GO") `
				-Or $line[0].Equals("HTML") `
				-Or $line[0].Equals("Groovy") `
				-Or $line[0].Equals("C++") `
				-Or $line[0].Equals("C") `
				-Or $line[0].Equals("C") `
				-Or $line[0].Equals("Perl"))
			{
				# Collate the langages and LOC
				$Languages = $Languages + $line[0] + " "
				$LOC = $LOC + $line[4]
			}
			elseif ($line[0].Equals("C/C++") `
				-Or $line[0].Equals("Objective") `
				)
			{
				# Collate the langages and LOC
				$Languages = $Languages + $line[0] + " " + $line[1] + "; "
				$LOC = $LOC + $line[5]
			}
			else 
			{
				$excludedLanguages = $excludedLanguages + $line[0] + "; "
			}
		
		}
		
		# Write the project, languages and LOC to a CSV file.
		
		if ($Languages.Equals("")) 
		{	
			$rVal = $name + "," + $excludedLanguages 
			Write-Output $rVal | Out-File -FilePath .\ClockReportException.csv -Append
		}
		else
		{
			$rVal = $name + "," + $Languages + "," + $LOC 
			Write-Output $rVal | Out-File -FilePath .\unifiedClockReport.csv -Append
		}
		$clocStreamreader.Dispose()
		
		# Check if flag is set to remove cloc report
		if ($deleteReport.Equals("true"))
		{
			Remove-Item .\$name.log
		}



		
		#exit(0)
}		
		$repoStreamreader.Dispose()

Write-Output "_____________________________________________________"
Write-Output ""
Write-Output "            Loading the Excel worksheet              "
Write-Output "     Please refresh the data table to see results    "
Write-Output "_____________________________________________________"

		
$FilePath = "C:/cxgit/License_Report.xlsx"

# Create an Object Excel.Application using Com interface
$objExcel = New-Object -ComObject Excel.Application

# Disable the 'visible' property so the document won't open in excel
$objExcel.Visible = $true

# Open the Excel file and save it in $WorkBook
$WorkBook = $objExcel.Workbooks.Open($FilePath)
				

exit(0)
