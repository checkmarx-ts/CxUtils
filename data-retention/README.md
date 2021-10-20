
# Data Retention

## Overview
Controls (Starts & Stops) data retention.  Given the URL of a specific Checkmarx web interface, starts a data retention by deleting either all scans within a specified date range or all but the last X scans for each project.

This command can also be used for stopping a currently running data retention process.

### Parameter Definitions 
|Parameter name	| Definition|
|---|---|
|configFile | Complete path to the data retention config (json) file. If not provided, the tool will attempt to load "data_retention_config.json" from the current working  directory. |
|v | Verbose output. |
|serviceUrl	| The URL of a Checkmarx web service.|
|username |	The Checkmarx user name of a user with permissions to run a data retention process (Server Administrator)|
|pass| The password of the specified Checkmarx user|
|serviceName| Windows Credentials Manager service name where Username and Password can be stored & retrieved securely instead of using -username and -pass parameters |
|StopRetention|	Enable this switch to stop the Data Retention process.|
|StartRetention|	Enable this switch to start the Data Retention process.|
|ByNumOfScans|	A switch defining that all of the scans in the system, except for the most recent X scans in each project, will be deleted. The number of recent scans to be kept (X) |is specified by the numOfScansToKeep parameter.|
|numOfScansToKeep|	When the ByNumOfScans switch is enables, defines how many recent scans are kept in each project when data retention is carried out.|
|ByDateRange|	A switch that defines that all of the scans within a specified date range will be deleted.|
|startDate|An optional inclusive lower limit of the date range of scans to delete. Only considers dates, ignores hours.|
|endDate	|A mandatory inclusive upper limit of the date range of scans to delete. Only considers dates, ignores hours.|
|ByRollingDate|	A switch that defines that all of the scans within a specified number of days from the current date will be deleted.|
|rollingDate|	A mandatory integer that is used to define the end date of the data retention by subtracting it from the current date.|
|retentionDurationLimit	|An optional parameter that allows to limit the duration of the data retention process. Specified only in round hours (integers), and applies to all scans performed after this parameter was set.|

### Configuration File
The powershell script is driven by a configuration file "data_retention_config.json" (default). It is also possible to explicitly provide a full path to a config file in a different folder (see -configFile parameter).
- The "log" section defines the logging timestamp format and the logging folder.
- The "cx" section defines the Checkmarx host and credentials to use for data retention. They can be overridden by parameters on the command line. If the "serviceUrl", "serviceName", "username", "pass" parameters are provided on the command line, they will take precedence over values configured in the json config file.
- The "dataRetention" section defines the default value for the duration limit for the data retention process. This can also be overridden in the command line by the "retentionDurationLimit" parameter.

### Examples
#### By Number of Scans

```CxManagement.ps1 -v -StartRetention -serviceUrl "http://domain.mysite.com/" -username "admin" -pass "p@ssw0rd" -ByNumOfScans -numOfScansToKeep 5```

```CxManagement.ps1 -v -StartRetention -serviceUrl "http://domain.mysite.com/" -serviceName "CxSAST" -ByNumOfScans -numOfScansToKeep 5```

```CxManagement.ps1 -v -configFile 'c:\cxutils\myDataRetentionConfig.json' -StartRetention -serviceUrl "http://domain.mysite.com/" -username "admin" -pass "p@ssw0rd" -ByNumOfScans -numOfScansToKeep 5```

```CxManagement.ps1 -v -StartRetention -serviceUrl "http://domain.mysite.com/" -username "admin" -pass "p@ssw0rd" -ByNumOfScans -numOfScansToKeep 5 -retentionDurationLimit 2```

```CxManagement.ps1 -v -StartRetention -serviceUrl "http://domain.mysite.com/" -username "admin" -pass "p@ssw0rd" -ByNumOfScans -numOfScansToKeep 5```


#### By Date Range

```CxManagement.ps1 -v -StartRetention -serviceUrl "http://domain.mysite.com/" -username "admin" -pass "p@ssw0rd" -ByDateRange -endDate "2015-10-10"```

```CxManagement.ps1 -v -StartRetention -serviceUrl "http://domain.mysite.com/" -serviceName "CxSAST" -ByDateRange -endDate "2015-10-10"```

```CxManagement.ps1 -v -StartRetention -serviceUrl "http://domain.mysite.com/" -username "admin" -pass "p@ssw0rd" -ByDateRange -startDate "2015-10-05" -endDate "2015-10-10"```


```CxManagement.ps1 -v -StartRetention -serviceUrl "http://domain.mysite.com/" -username "admin" -pass "p@ssw0rd" -ByDateRange -startDate "2015-10-05" -endDate "2015-10-10" -retentionDurationLimit 2```


#### By Rolling Date

```CxManagement.ps1 -v -StartRetention -serviceUrl "http://domain.mysite.com/" -username "admin" -pass "p@ssw0rd" -ByRollingDate -rollingDate 180```

```CxManagement.ps1 -v -StartRetention -serviceUrl "http://domain.mysite.com/" -serviceName "CxSAST" -ByRollingDate -rollingDate 180```

#### Stop Data Retention

``` CxManagement.ps1 -v -StopRetention -serviceUrl "http://domain.mysite.com/" -username "admin" -pass "p@ssw0rd" ```

``` CxManagement.ps1 -v -StopRetention -serviceUrl "http://domain.mysite.com/" -serviceName "CxSAST" ```

### Notes
- In case -serviceName is used, it is required to install the Powershell module 'CredentialManager', which you can do with following command (with admin privileges):
 ```ps1
    Install-Module -Name "CredentialManager" 
 ```
- It is only possible to define either StartRetention -OR- StopRetention.
- It is only possible to define one type of retention at a time.
- The duration limit is not an immediate limit, scans are deleted in bulks of X (configured in the database with a default value of 3) and the data retention will only stop at the end of a bulk.

#### Execution Policy
* If you are having trouble executing the script, change your execution policy (Set-ExecutionPolicy Unrestricted) or use what we'll probably tell clients to do :

Use the "Bypass" Execution Policy Flag.  This is a nice flag added by Microsoft that will bypass the execution policy when you're executing scripts from a file. When this flag is used Microsoft states that "Nothing is blocked and there are no warnings or prompts". This technique does not result in a configuration change or require writing to disk.

PowerShell.exe -ExecutionPolicy Bypass -File .runme.ps1
Other methods can be found in - https://blog.netspi.com/15-ways-to-bypass-the-powershell-execution-policy./

### Automation of Data Retention script with Task Scheduler

In order to schedule data retention to run often on a weekly or monthly basis we can use the Windows Task Scheduler.
You need to perfom the following actions:
- Open "Task Scheduler"
- Create Basic Task...
    - Name: CxWeeklyDataRetention
    - Description: Checkmarx Weekly Data Retention
    - Next >
    - Trigger: Weekly
    - Next >
    - Select the expected day and time to run data retention
    - Next >
    - Action: Start a program
    - Next >
    - Program/script: powershell
    - Add arguments(optional): -windowstyle hidden -command C:\path_to_folder\CxManagement.ps1 -StartRetention -serviceUrl "http(s)://server" -serviceName "CxSAST" -ByNumOfScans -numOfScansToKeep 5
    - Finish
- Then, press Run to check if Task is working in Data Retention page on the Portal.
- If you can see data retention has run, Task was successfully automated !