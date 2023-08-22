# engineering-health-check

## Checkmarx One

The `cxInsight_CxOne.ps1` PowerShell script is used to retrieve scan data from a Checkmarx One tenant for Insight Analysis in the Engineering Health Check.
The script collects scan Information that includes data about: Projects, Presets, Teams, Engines, and Result Metrics

### cxInsight_CxOne.ps1 usage

Open PowerShell and enter the following command
```
.\cxInsight_CxOne.ps1
```

* At the prompt, enter the API key for the Checkmarx One tenant.

The `cxInsight_CxOne.ps1` script accepts the following command line options:

| Option | Requires Argument | Default | Description |
|--------|-------------------|---------|-------------|
| `-ApiKey` | Yes | None | The ApiKey |
| `-DaySpan` | Yes | 90 |The number of days' of data to collect |
| `-EndDate` | Yes | The current date | The end date of the period for which to collect data |
| `-ExclProjectName` | No | False | If specified, the project name is not included in the extracted data |
| `-Limit` | Yes | 200 | The number of items to retrieve in each API call |
| `-ScanId` | Yes | The scan identifier | If this option is specified, only data for the specified scan is retrieved, and the output is written to the console |
| `-Quiet` | No | False | If specified, a completion message will not be printed when the script finishes |
| `-StartDate` | Yes | 90 days before the current date | The start date of the period for which to collect data |

The `cxInsight_CxOne.ps1` script also accepts the following standard PowerShell command line options.

| Option | Requires Argument | Default | Description |
|--------|-------------------|---------|-------------|
| `-Debug` | No | N/A | Enable debug messages. **Note:** this will cause the decoded API Key and the bearer token to be printed. |
| `-Verbose` | No | N/A | Enable verbose messages. |

To get more information about the usage, use the `Get-Help` command:
```
Get-Help .\cxInsight_CxOne.ps1
```

## Checkmarx SAST

The `cxInsight_8_9.ps1` and `cxInsight_9_0.ps1` PowerShell scripts are used to retrieve CxSAST Scan Data for Insight Analysis in the Engineering Health Check.
The scripts collect scan Information that includes data about: Projects, Presets, Teams, Engines, and Result Metrics
The script also optionally collects and generates a summary of the result data for the last full scan of each project. Note that it is possible for the last scan of a project to have no results (e.g., if there were no code changes).

* Use the corresponding script for the version of CxSAST that is installed.
* Ensure admin privileges before running the scripts


### cxInsight_X_X.ps1 usage
Open PowerShell and enter the following replacing X_X with the correct version
```
.\cxInsight_X_X.ps1
```
* Enter the CxServer Url - ex: https://acme.checkmarx.net
* Enter administrator credentials for CxSAST

To get more information about the usage, use the `Get-Help` command:
```
Get-Help .\cxInsight_X_X.ps1
```

### Credential Prompt via Command Line

The script prompts for a CxSAST username and password. If your environment does not have GUI support then you should first enable console prompting.

```powershell
$key = "HKLM:\SOFTWARE\Microsoft\PowerShell\1\ShellIds"
Set-ItemProperty $key ConsolePrompting True
```

### Triage Results

When running the cxInsight_X_X.ps1 script, you must explicitly decide whether to retrieve triage results. To retrieve triage results, pass the `-Results` command line switch:

```
.\cxInsight_X_X.ps1 -Results
```

To exclude the triage results, use the `-ExclResults` command line switch:

```
.\cxInsight_X_X.ps1 -ExclResults
```

The `-ExclResults` switch takes precedence over the `-Results` switch.

### Excluding Project and Team Name

The `-ExclProjectName` and `-ExclTeamName` command line switches can be used to prevent the inclusion of the project name and the team name, respectively, in the scan data.

For convenience, the `-ExclAll` command line switch can be used to suppress the retrieval of result data and the suppression of the project and team names.

### LDAP Users

It is possible to use the credentials of an LDAP user to run the `cxInsight_X_X.ps1` script. In this case, the username passed to the script should be of the form *authentication provider name\username*. The authentication provider name can be seen in the “Sign in method” dropdown menu of the CxSAST portal’s login screen.

Note that it is not possible to use the credentials of a SAML user.

### Permissions

The user whose credentials are used to run the `cxInsight_X_X.ps1` script must be assigned a role that has the Sast API permission (needed as the script uses the CxSAST OData API). This is the only permission required.
