<#
.SYNOPSIS
    This script submits a forced scan with the CxCli for Projects listed in a CSV file.

.DESCRIPTION
    This script is intended to run from a CxManager server or similar environment where the 
    "CxSrc" folder is available to the script. The script loops over a CSV file with 
    structure (and example data) like this:

        TeamName, ProjectName, SourcePath
        CxServer, dvna zip, 1_0000000015_0-2120404009_000662179826
        CxServer, diva-android, 3_0000000063_000-99565538_000573355075

    It is important that the TeamName, Projectname, and SourcePath headers exist and are named
    exactly like this. The fields are:

    TeamName:    The full team name of the project.
    ProjectName: The name of the project.
    SourcePath:  The SourcePath, taken from the database, of the source code that should be scanned
                 for this project. This path is combined with the CxSrcPath script argument to find
                 the source code to be submitted for the scan.

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

.EXAMPLE

    $credential = Get-Credential
    cxsast-force-scans.ps1 -server "https://cxsast.company.tld/" `
                           -username "$($credential.GetNetworkCredential().UserName)" `
                           -password "$($credential.GetNetworkCredential().Password)" `
                           -csvFile "C:\temp\force-scans\projects-to-scan.csv" `
                           -CxSrcPath "\\amznfsxrnhkbrjw.corp.local\share\CxSrc" 

.NOTES
    This script performs a syncronous scan so as to not overwhelm the system.
    
    Consider batching up the work into multiple CSV files and running this script multiple times
    to help control the throughput. 


    To create the CSV file, adapt this query to find the projects source examples of interest you want to
    force a scan for. Note the SourcePath is the combination of the Project ID, an underscore, and the Source ID.

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
    

    See https://checkmarx.atlassian.net/wiki/spaces/SD/pages/914096139/CxSAST+CxOSA+Scan+v8.9.0 for a CLI reference.
                          
#>
param (
    [Parameter(Mandatory=$True)]   [string] $server,
    [Parameter(Mandatory=$True)]   [string] $username,
    [Parameter(Mandatory=$True)]   [string] $password,
    [Parameter(Mandatory=$True)]   [String] $csvFile,
    [Parameter(Mandatory=$True)]   [String] $CxSrcPath,
    [Parameter(Mandatory=$False)]  [String] $url = "https://download.checkmarx.com/9.0.0/Plugins/CxConsolePlugin-2021.1.1.zip",
    [Parameter(Mandatory=$False)]  [String] $Destination = "C:\temp\force-scans\CxConsolePlugin-2021.1.1"
)

# Force TLS 1.2 in this session
[System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072;

# Show no status bars
$progressPreference = 'silentlyContinue'


# Downloads and extracts the CxCli plugin.
function Download-CxCliPlugin {
    param (
        [Parameter(Mandatory=$True)] [String] $url,
        [Parameter(Mandatory=$True)] [String] $Destination
    )

    $zipFilename = $url.Substring($url.LastIndexOf("/") + 1)

    if (!(Test-Path -Path $Destination)) {
        Write-Host "$(Get-Date) creating ${Destination}"
        md $Destination
    }
    
    if (!(Test-Path (Join-Path $Destination -ChildPath $zipFilename))) {

        Write-Host "$(Get-Date) Downloading ${url} to ${Destination}"
        (New-Object System.Net.WebClient).DownloadFile($url, (Join-Path $Destination -ChildPath $zipFilename))

        Write-Host "$(Get-Date) Extracting $zipFileName"
        Expand-Archive -Path (Join-Path $Destination -ChildPath $zipFilename) -DestinationPath $Destination
    }
}


# Download the CLI if it is not already downloaded
Download-CxCliPlugin -url $url -Destination $Destination

# Find the CLI executable
$cx = Get-ChildItem -Path C:\ -Filter "runCxConsole.cmd" -Recurse -ErrorAction SilentlyContinue | Sort -Descending | Select -First 1 -ExpandProperty FullName

# Validate the CLI
if (($null -eq $cx) -or -not (Test-Path -Path $cx -PathType Leaf)) {
    Throw "runCxConsole.cmd not found in ${Destination}."
}

# Validate the CSV file exists
if (!(Test-Path -Path $csvFile -PathType Leaf)) {
    Throw "A file was not found at ${csvFile}."
}

# Validate the CxSrc folder
if (!(Test-Path -Path $CxSrcPath -PathType Container)) {
    Throw "A folder does not exist at ${CxSrcPath}."
}


# Validate the CSV File first and exit with any error. 
$validationLine = 0
Import-Csv $csvFile | ForEach-Object {
    $validationLine++

    if ($null -eq $_.TeamName) {
        Throw "Error processing $_ - a TeamName field does not exist on line ${validationLine}."
    }
    if ($null -eq $_.ProjectName) {
        Throw "Error processing $_ - a ProjectName field does not exist on line ${validationLine}."
    }
    if ($null -eq $_.SourcePath) {
        Throw "Error processing $_ - a SourcePath field does not exist on line ${validationLine}."
    }


    if ([String]::IsNullOrEmpty($_.TeamName)) {
        Throw "Error processing $_ - a TeamName has no value on line ${validationLine}."
    }
    if ([String]::IsNullOrEmpty($_.ProjectName)) {
        Throw "Error processing $_ - a TeamName has no value on line ${validationLine}."
    }
    if ([String]::IsNullOrEmpty($_.SourcePath)) {
        Throw "Error processing $_ - a TeamName has no value on line ${validationLine}."
    }
}


# Process each line in the CSV file and submit a force scan.
Import-Csv $csvFile | ForEach-Object {

    $fqpn = "$($_.TeamName)\$($_.ProjectName)"
    Write-Host "$(Get-Date) Processing $fqpn"

    # Run the CLI tool. Using "Scan" the CLI will perform a syncronous scan which means the CLI will monitor the scan progress
    # and block execution of this script until the scan completes. You can also use "AsyncScan" which will submit the scan, wait
    # for just a moment while the scan is accepted, and then exit. 
    & "$cx" Scan -v -projectName "$fqpn" -CxServer "$server"  -CxUser "$Username" -CxPassword "$Password" -LocationType Folder -LocationPath "$(Join-Path -Path $CxSrcPath -ChildPath $_.SourcePath)" -ForceScan
}


Write-Host "$(Get-Date) Finished"
