## cxsast_mass_testscan
This repository has scripts for scanning using CxFlow or CxCLI.  The scripts ingest a text file of public git repos.

## Usage 

## Scan_Git for Windows using Powershell
scan_git.ps1 is a powershell script that allows a git clone of multiple git repos from a text file and a scan via the CLI or CxFlow
 

# Environment Prep for Scan_Git Powershell for Windows

* Install Chocolatey - https://chocolatey.org/install
* Open a CMD prompt as admin
* Replace the following user directory with yours

```
choco install -y wget unzip
cd C:\Users\CxAdmin
mkdir CxConsole && cd ./CxConsole

#Latest public CxCLI
wget -O cli.zip https://download.checkmarx.com/9.0.0/Plugins/CxConsolePlugin-2020.2.18.zip && unzip cli.zip && del cli.zip

```
* Update the .ps1 script values $CxServer, $CxTeam, $CLI  
* To get token run the following command and replace with your login info
```
. .\scan_git.ps1; GetToken -CxUser admin -CxPass P@ssword1
```

* Update the .ps1 script value $CxToken
* Update the .txt file of choice and run the following command to scan 

```
. .\scan_git.ps1; AsyncScan -gitList giturls.txt
```
# Prep for Windows using CxFlow
```
choco install -y wget unzip
cd C:\Users\CxAdmin
mkdir CxFlow && cd ./CxFlow

#latest stable release
wget -O cxflow.jar https://github.com/checkmarx-ltd/cx-flow/releases/download/1.5.4/cx-flow-1.5.4.jar

#prerelease
wget -O cxflow.jar https://github.com/checkmarx-ltd/cx-flow/releases/download/1.6.0/cx-flow-1.6.0.jar

```
* Update username, password, team, base-url in the application-scan.yml file 
* Update the .txt file of choice and run the following command to scan 

```
. .\scan_git.ps1; FlowScan -gitListFilePath giturls.txt
```

## Scan_Git_CxFlow for Linux using CxFlow
scan_git_cxflow.sh is a bash script that allows a git clone of multiple git repos from a text file and a scan via CxFlow 

* Install wget 
* Update username, password, team, base-url in the application-scan.yml file 
* Update the .txt file of choice and run the following command to scan

```
#latest stable release
wget -O cxflow.jar https://github.com/checkmarx-ltd/cx-flow/releases/download/1.5.4/cx-flow-1.5.4.jar

#prerelease
wget -O cxflow.jar https://github.com/checkmarx-ltd/cx-flow/releases/download/1.6.0/cx-flow-1.6.0.jar

sh scan_git_cxflow giturls.txt
```

# Authors
Sam Quakenbush, Sales Engineering - Initial work

# License
This project is licensed under TBD

