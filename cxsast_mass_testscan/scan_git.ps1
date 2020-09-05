<# Usage
. ./scan_git.ps1; AsyncScan -gitList giturls.txt
giturls.txt is the file containing the GIT URLs on each line.

Test command to use before running script on large amount of repos
. ./scan_git.ps1; TestCLI
#>

#Replace variables with appropriate values
$CLI = 'C:\Users\CxAdmin\CxConsole\runCxConsole.cmd'
$Team = 'CxServer\SP\Company\Demo\'
$CxServer = 'http://localhost'
$CxToken = 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'

#CxFlow
$Flow = 'C:\Users\CxAdmin\CxFlow\cxflow.jar'
$clonefolder = 'C:\Users\CxAdmin\CxFlow\clonefolder'

#optional update
$exclusions = '*test*,*lib*,*docs*,*swagger*,*angular*,*node_modules*,*bootstrap*,*modernizer*,*yui*,*dojo*,*xjs*,*react*,*plugins*,*3rd*,*build*,*nuget*'
$flowexclusions ='test,lib,docs,swagger,angular,node_modules,bootstrap,modernizer,yui,dojo,xjs,react,plugins,3rd,build,nuget'


function AsyncScan 
{
  param (
    [Parameter(Mandatory = $True)]
    [string]$gitList
      )

  foreach($line in Get-Content $gitList) {
    $gitUrl = $line
    $gitName = $gitUrl.Substring($gitUrl.LastIndexOf("/") + 1)
    $Project = [IO.Path]::GetFileNameWithoutExtension($gitName)
  
    . $CLI AsyncScan -v -Projectname $Team$Project -CxServer $CxServer -CxToken $CxToken -LocationType git -LocationURL $gitUrl -LocationBranch refs/heads/master -locationpathexclude $exclusions -forcescan
  }
  
}

function GetToken
{
  param
  (
    [Parameter(Mandatory = $True)]
    [ValidateNotNullOrEmpty()]
    [String]
    $CxUser = "",
    
    [Parameter(Mandatory = $True)]
    [ValidateNotNullOrEmpty()]
    [String]
    $CxPass = ""
  )
 . $CLI GenerateToken -v -CxUser $CxUser -CxPassword $CxPass -CxServer $CxServer
}

function FlowScan 
{
  param (
    [Parameter(Mandatory = $True)]
    [string]$gitList
      )

  foreach($line in Get-Content $gitList) {
    git clone $line $clonefolder
    $gitName = $line.Substring($line.LastIndexOf("/") + 1)
    $Project = [IO.Path]::GetFileNameWithoutExtension($gitName)
    # Added 'cd' command to satisfy $clonefolder relative path
	  cd C:\Users\CxAdmin\CxFlow
    java -jar $Flow --spring.config.location="./application-scan.yml" --scan --f=$clonefolder --cx-project=$Project --app=$Project --forcescan  --exclude-folders=$flowexclusions
    Remove-Item $clonefolder -recurse -force
    Remove-Item * -Filter *.zip -force
  }
  
}

function TestCLI($gitList='test.txt')
{
  AsyncScan($gitList)
}

function TestFlow($gitList='./GitLists/test.txt')
{
  FlowScan($gitList)
}