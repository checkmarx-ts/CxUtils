# Synopsis
Used to update a existing preset with a new one across all projects

# Description
This script will produce a report of the Scan settings for all projects as a 
CSV file or to update a selected preset to the new preset across all projects.

The script prompts for a CxSAST username and password. If your environment does not have GUI support then you should first enable console prompting.

    $key = "HKLM:\SOFTWARE\Microsoft\PowerShell\1\ShellIds"
    Set-ItemProperty $key ConsolePrompting True

## Usage
Help
    C:\Users\Administrator\Desktop\ModifyPreset.ps1 [-help] [<CommonParameters>]
    
Reporting
    C:\Users\Administrator\Desktop\ModifyPreset.ps1 [-filePath <String>] -baseURI <String> [-teamNameFilter <String[]>] [<CommonParameters>]
    C:\Users\Administrator\Desktop\ModifyPreset.ps1 [-filePath <String>] -baseURI <String> [-teamIdFilter <Int32[]>] [<CommonParameters>]    

Update   
    C:\Users\Administrator\Desktop\ModifyPreset.ps1 [-update] -baseURI <String> [-teamIdFilter <Int32[]>] -currentPreset <String> -newPreset <String> [<CommonParameters>]  
    C:\Users\Administrator\Desktop\ModifyPreset.ps1 [-update] -baseURI <String> [-teamNameFilter <String[]>] -currentPreset <String> -newPreset <String> [<CommonParameters>]

## Notes
Version:*Tabspace*3.0

Date:*Tabspace*28/07/2023

Written by:*Tabspace*Michael Fowler

Contact:*Tabspace*michael.fowler@checkmarx.com

## Change Log
Version    Detail
-----------------
1.0*Tabspace*Original version

2.0*Tabspace*Removed username and password parameters and replaced with credentials   
*Tabspace*Added Team filters to filter results by arrays of Team IDs or Team Names
           
3.0*Tabspace*Added logic to handle additional values introduced in API v4 and stop these being overridden         

## Parameters
```

.PARAMETER help
Display help

.PARAMETER update
Determines if you are updating a selected preset or running a report.
When not specified a report will be run

.PARAMETER filePath
Allows you to set the path and filename for the generated report. If not specified will default to nameing the file
Scan Settings Report.csv and saving it to the location of the script

.PARAMETER baseURI
Specifies the URL used to connect to the CxSAST instance.
Is mandatory and will prompt when not specified

.PARAMETER teamNameFilter
Specifies a comma seperated list of Team names to filter the results on
Cannot be used with teamIdFilter

.PARAMETER teamIdFilter
Specifies a comma seperated list of Team names to filter the results on
Cannot be used with teamNameFilter

.PARAMETER username
Specifies the username used to authenticate to the CxSAST instance.
User should have access to all projects
Is mandatory and will prompt when not specified

.PARAMETER password
Specifies the password associated with the selected username.
Is mandatory and will prompt when not specified

.PARAMETER currentPreset
The preset which will be replaced to the new preset
Is mandatory when update is used and will prompt when not specified

.PARAMETER newPreset
The preset which will replace the current preset
Is mandatory when update is used and will prompt when not specified

```