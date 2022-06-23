# engineering-health-check

These Powershell scripts are used to retrieve  CxSAST Scan Data for Insight Analysis in the Engineering Health Check.
The script will collect scan Information that includes data about: Projects, Presets, Teams, Engines, and Result Metrics
The 9.x version of the script also optionally collects and generates a summary of the result data for the last scan of each project. Note that it is possible for the last scan of a project to have no results (e.g., if there were no code changes).

* Use the corresponding script for the version of CxSAST that is installed.
* Ensure admin privileges before running the scripts


## cxInsight_XX.ps1 usage
Open powershell and enter the following replacing XX with the correct version
```
./cxInsight_XX.ps1
```
* Enter the CxServer Url - ex: https://acme.checkmarx.net
* Enter administrator credentials for CxSAST

To get more information about the usage, use the `Get-Help` command:
```
Get-Help ./cxInsight_XX.ps1
```

## Credential Prompt via Command Line

The script prompts for a CxSAST username and password. If your environment does not have GUI support then you should first enable console prompting.

```powershell
$key = "HKLM:\SOFTWARE\Microsoft\PowerShell\1\ShellIds"
Set-ItemProperty $key ConsolePrompting True
```
