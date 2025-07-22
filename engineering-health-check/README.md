# engineering-health-check

These Powershell scripts are used to retrieve  CxSAST Scan Data for Insight Analysis in the Engineering Health Check.
The script will collect scan Information that includes data about: Projects, Presets, Teams, Engines, and Result Metrics. The 9.0 version of the script also retrieves license data (if the SAST version supports this) and engine information.
The script also optionally collects and generates a summary of the result data for the last full scan of each project. Note that it is possible for the last scan of a project to have no results (e.g., if there were no code changes).

* Use the corresponding script for the version of CxSAST that is installed.
* Ensure admin privileges before running the scripts


## cxInsight_X_X.ps1 usage
Powershell execution policies on the local machine may prevent the execution of the Engineering Health Check powershell scripts. 
Open Powershell as an administrator and execute the following to ublock execution of the Checkmarx scripts. This unblocks the specified scripts only and does not update the current execution policies.
```
Unblock-File -Path ./cxInsight*.ps1
```
Next, enter the following replacing X_X with the correct version
```
./cxInsight_X_X.ps1
```
* Enter the CxServer Url - ex: https://acme.checkmarx.net
* Enter administrator credentials for CxSAST

To get more information about the usage, use the `Get-Help` command:
```
Get-Help ./cxInsight_X_X.ps1
```

## Credential Prompt via Command Line

The script prompts for a CxSAST username and password. If your environment does not have GUI support then you should first enable console prompting.

```powershell
$key = "HKLM:\SOFTWARE\Microsoft\PowerShell\1\ShellIds"
Set-ItemProperty $key ConsolePrompting True
```

## Triage Results

When running the cxInsight_X_X.ps1 script, you must explicitly decide whether to retrieve triage results. To retrieve triage results, pass the `-Results` command line switch:

```
.\cxInsight_X_X.ps1 -Results
```

To exclude the triage results, use the `-ExclResults` command line switch:

```
.\cxInsight_X_X.ps1 -ExclResults
```

The `-ExclResults` switch takes precedence over the `-Results` switch.

## Excluding Project and Team Name

The `-ExclProjectName` and `-ExclTeamName` command line switches can be used to prevent the inclusion of the project name and the team name, respectively, in the scan data.

For convenience, the `-ExclAll` command line switch can be used to suppress the retrieval of result data and the suppression of the project and team names.

## LDAP Users

It is possible to use the credentials of an LDAP user to run the `cxInsight_X_X.ps1` script. In this case, the username passed to the script should be of the form *authentication provider name\username*. The authentication provider name can be seen in the “Sign in method” dropdown menu of the CxSAST portal’s login screen.

Note that it is not possible to use the credentials of a SAML user.

## Permissions

The user whose credentials are used to run the `cxInsight_X_X.ps1` script must be assigned a role that has the Sast API permission (needed as the script uses the CxSAST OData API). This is the only permission required.

## Troubleshooting

This section contains some tips on troubleshooting the
`cxInsight_X_X.ps1` script.

### Unable to retrieve Checkmarx AC Token

Sometimes, the `cxInsight_9_0.ps1` script will fail to retrieve the
access token needed for subsequent API requests. Here an example of
the script’s output when this happens:

```
Running Script on Version  5.1.26100.4652
Exception: The remote server returned an error: (400) Bad Request.
StatusCode: 400
StatusDescription: Bad Request
Unable to retrieve Checkmarx AC Token
```

The first thing to check is the Access Control trace log on the CxSAST
manager server. This will be in the `<CxSAST Install
Path>\Logs\AccessControl\Trace` folder. If the problem is with the
username, a log message like the following will be present.

```
2025-07-22 23:27:47.043 [ThreadId: 23] [Warning] [Cx.AccessControl.Infrastructure.IdentityServer.Validators.ResourceOwnerPasswordValidator] Failed to find user with the requested username.
```

If the problem is with the password, a log message like the following
will be present.

```
2025-07-22 23:28:50.833 [ThreadId: 28] [Warning] [Cx.AccessControl.Infrastructure.IdentityServer.Validators.ResourceOwnerPasswordValidator] Failed to validate password for user.
```

For obvious reasons, the script does not print the credentials to the
screen. However, if you want to validate that it is indeed using the
correct credentials, after the following line:

```
$cxPassword = $cred.GetNetworkCredential().password
```

Add:

```
Write-Host "Username: ${cxUsername}, password: ${cxPassword}"
```

## Scans Created When Branching Projects

When a project is branched in CxSAST, a duplicate scan record is made
of the last scan completed before the branching. This means that, if a
project was both scanned and branched during the period for which the
enginerring health check data was extracted, the resultant
`scan-data.json` file will contain two entries for the same scan.

The `split_branch_scans.ps1` script can be used to split the
`scan-data.json` file into two files, one containing the /base/ scans,
and the other containing the /branched/ scans. These files will be
named `scan-data-base.json` and `scan-data-branch.json`
respectively. The recors in the latter file will include an additional
property, `OrigScanId`, which gives the number of the corresponding
scan in the /base/ file.

### Usage

The `split_branch_scans.ps1` script expects the name of the file
containing the original scan data to be passed on the command line:

```
PS C:\...\ehc> .\split_branch_scans.ps1 -FileName scan-data.json
