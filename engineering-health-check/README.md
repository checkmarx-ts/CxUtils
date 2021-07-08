# engineering-health-check

These Powershell scripts are used to retrieve  CxSAST Scan Data for Insight Analysis in the Engineering Health Check.
The script will collect scan Information that includes data about: Projects, Presets, Teams, Engines, and Result Metrics 

* Use the corresponding script for the version of CxSAST that is installed.
* Ensure admin priviledges before running the scripts


cxInsight_XX.ps1 usage
Open powershell and enter the following replacing XX with the correct version
```
./cxInsight_XX.ps1
```
* Enter the CxServer Url - ex: https://acme.checkmarx.net
* Enter administrator credentials for CxSAST


## Credential Prompt via Command Line

The script prompts for a CxSAST username and password. If your environment does not have GUI support then you should first enable console prompting. 

```powershell
$key = "HKLM:\SOFTWARE\Microsoft\PowerShell\1\ShellIds"
Set-ItemProperty $key ConsolePrompting True
```
