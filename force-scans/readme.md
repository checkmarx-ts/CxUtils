# Synopsis
This script submits a forced scan with the CxCli for Projects listed in a CSV file. It can be used to force a rescan using the latest source code available for a given set of projects. 

# Description
 This script is intended to run from a CxManager server or similar environment where the 
    "CxSrc" folder is available to the script. The script loops over a CSV file with 
    structure (and example data) like this:
```
TeamName, ProjectName, SourcePath
CxServer, dvna zip, 1_0000000015_0-2120404009_000662179826
CxServer, diva-android, 3_0000000063_000-99565538_000573355075
```
It is important that the TeamName, Projectname, and SourcePath headers exist and are named
exactly like this. The fields are:

CSV Column | Description
---|---
`TeamName` |    The full team name of the project.
`ProjectName `| The name of the project.
`SourcePath` |  The SourcePath, taken from the database, of the source code that should be scanned for this project. This path is combined with the CxSrcPath script argument to find the source code to be submitted for the scan.

## Parameters
```
.PARAMETER server
    The URL to the CxSAST Server, including protocol e.g. https://sast.company.com.

.PARAMETER username
    The username to submit scans with.

.PARAMETER password
    The password for the username.

.PARAMETER csvFile
    The aboslute path to the CSV File to process.

.PARAMETER CxSrcPath
    The absolute path to the CxSrc folder root.

.PARAMETER url
    Optional. The url to the CxCLI plugin which will be downloaded.

.PARAMETER Destination
    Optional. The local folder to download and unzip the CxCLI plugin to.
```

## Example

```
$credential = Get-Credential
cxsast-force-scans.ps1 -server "https://cxsast.company.tld/" `
                       -username "$($credential.GetNetworkCredential().UserName)" `
                       -password "$($credential.GetNetworkCredential().Password)" `
                       -csvFile "C:\temp\force-scans\projects-to-scan.csv" `
                       -CxSrcPath "\\amznfsxrnhkbrjw.corp.local\share\CxSrc" 
```

## Notes
This script performs a syncronous scan so as to not overwhelm the system.

Consider batching up the work into multiple CSV files and running this script multiple times
to help control the throughput. 


To create the CSV file, adapt this query to find the projects source examples of interest you want to
force a scan for. Note the SourcePath is the combination of the Project ID, an underscore, and the Source ID.

```
SELECT p.Name as ProjectName, 
        t.FullName as TeamName,
      concat(p.id, '_', ts.SourceId) as SourcePath, ts.StartTime, ts.Comment
FROM [CxDB].[dbo].[Projects] p 
inner join [CxDB].[dbo].[TaskScans] ts on ts.ProjectId = p.ID
inner join [cxdb].[CxEntities].[Team] t on t.Id = p.Owning_Team
where ts.Id in (select max(ts1.id) from [cxdb].[dbo].[TaskScans] ts1 where ts1.ProjectId = p.ID)  -- most recent scan for a project

-- This clause filters out projects that have had a scan in the last 30 days
and p.id not in (select ProjectId from [cxdb].[dbo].[TaskScans] ts2 where 
                 ts2.StartTime BETWEEN DATEADD(dd,-30, GETDATE()) AND GETDATE() 
         and ts2.comment not like '%Attempt to perform scan on%No code changes were detected%')
 ```   

 See https://checkmarx.atlassian.net/wiki/spaces/SD/pages/914096139/CxSAST+CxOSA+Scan+v8.9.0 for a CLI reference.
