<#
.SYNOPSIS
Search utility that searches for given library in SCA search results across scans and projects.

.DESCRIPTION
This script searches for libraries (vulnerable or not) across scans (including historical) and projects across the organization.


.PARAMETER dbUser
    Database account that can read from the Checkmarx database. 
    OPTIONAL: Skip if using Integrated Authentication on the Checkmarx database
.PARAMETER dbPass
    Password for the database account that can read from the Checkmarx database
    OPTIONAL: Skip if using Integrated Authentication on the Checkmarx database
.PARAMETER lib
    The library name to search for. Ex. log4j
.PARAMETER group
    Grouping to use while displaying results on the console. Valid values are [Team | Project]. Ignored if used in conjunction with the -json flag.
.PARAMETER json
    If this flag is specified, search results will be written to a JSON file on disk.
.PARAMETER grid
    If this flag is specified, search results will be rendered in a Powershell Grid View.


.EXAMPLE
.\cx-sca-search.ps1 -lib log4j
.\cx-sca-search.ps1 -lib log4j -group Team
.\cx-sca-search.ps1 -lib log4j -group Project
.\cx-sca-search.ps1 -lib log4j -json
.\cx-sca-search.ps1 -dbUser dbaccount -dbPass sec$@t123 -lib log4j


.NOTES
Version 1.0, Gem Immauel (gem.immanuel@checkmarx.com), Checkmarx Professional Services

The command line parameters will override the values read from the 
configuration file (cx_sca_search_config.json)

#>
[CmdletBinding(DefaultParametersetName = 'None')] 
Param(
    [Parameter(ParameterSetName = 'SQLServerAuth', Mandatory = $False, HelpMessage = "Database account to connect to the Checkmarx database (SQLServer Auth)")]
    [ValidateNotNullOrEmpty()]
    [String]
    $dbUser = "",
    
    [Parameter(ParameterSetName = 'SQLServerAuth', Mandatory = $True, HelpMessage = "Database account password (SQLServer Auth)")]
    [ValidateNotNullOrEmpty()]
    [String]
    $dbPass = "",  
    
    [Parameter(Mandatory = $True, HelpMessage = "Library name to search for.")]
    [ValidateNotNullOrEmpty()]
    [String]
    $lib = "",

    [Parameter(Mandatory = $False, HelpMessage = "Groups search results for display either by Team or Project.")]
    [ValidateSet('Project', 'Team')]
    [String]
    $group = "",

    [Parameter(Mandatory = $False, HelpMessage = "Render search results as JSON and write to file on disk.")]
    [switch] 
    $json,

    [Parameter(Mandatory = $False, HelpMessage = "Render search results in a Powershell Grid View")]
    [switch] 
    $grid
)

# This assumes that the SqlServer powershell module is already installed.
# If not, run "Install-Module -Name Invoke-SqlCmd2" as an administrator prior to running this script.
Import-Module "Invoke-SqlCmd2" -DisableNameChecking 

# -----------------------------------------------------------------
# DateTime Utility
# -----------------------------------------------------------------
Class DateTimeUtil {

    # Gets timestamp in UTC in configured format
    [String] NowUTCFormatted() {
        return $this.Format($this.NowUTC())
    }

    # Gets timestamp in UTC
    [DateTime] NowUTC() {
        return (Get-Date).ToUniversalTime()
    }

    # Converts to UTC and formats
    [String] ToUTCAndFormat([DateTime] $dateTime) {
        return $this.Format($dateTime.ToUniversalTime())
    }
    
    # Formats time based on configured format
    [String] Format([DateTime] $dateTime) {
        return $dateTime.ToString($script:config.cx.timeFormat)
    }
}

# -----------------------------------------------------------------
# Input/Output Utility
# -----------------------------------------------------------------
Class IO {
    
    # General logging
    static [String] $LOG_FILE = "cx_sca_search.log"
    hidden [DateTimeUtil] $dateUtil = [DateTimeUtil]::new()

    # Files for JSON output 
    static [String] $FILE_SUFFIX_TIMESTAMP_FORMAT = "yyyyMMdd_hhmmssfff"

    # Logs given message to configured log file
    Log ([String] $message) {
        # Write to log file
        $this.WriteToFile($message, [IO]::LOG_FILE) 
        # Also write to console
        $this.Console($message)
    }

    # Write given string to host console
    Console ([String] $message) {
        Write-Host $this.AddTimestamp($message)
    }

    # Write a pretty header output
    WriteHeader() {
        $this.Console("-----------------------------------------")
        $this.Log("Checkmarx SCA Search")
        $this.Log("Database: $($script:config.cx.db.instance)")
        if ($script:config.cx.db.username -and $script:config.cx.db.password) {
            $this.Log("Using SQLServer Authentication")
        }
        else {
            $this.Log("Using Integrated Authentication to SQLServer")
        }

        $this.Console("-----------------------------------------")
    }
    
    # Utility that writes to given file
    hidden WriteToFile([String] $message, [String] $file) {
        Add-content $file -Value $this.AddTimestamp($message)
    }

    hidden [String] AddTimestamp ([String] $message) {
        return $this.dateUtil.NowUTCFormatted() + ": " + $message
    }

    # Write to JSON file
    WriteJSON([PSCustomObject] $object) {
        
        # Ensure folder exists
        [String] $jsonOutDir = $script:config.log.jsonDirectory
        If (!(Test-Path $jsonOutDir)) {
            New-Item -ItemType Directory -Force -Path $jsonOutDir
        }
        $jsonOutDir = (Get-Item -Path $jsonOutDir).FullName

        # Create timestamp 
        [DateTime] $timestamp = $this.dateUtil.NowUTC()
        [String] $fileSuffix = $timestamp.ToString([IO]::FILE_SUFFIX_TIMESTAMP_FORMAT)

        # Create file name
        [String] $fileName = "$fileSuffix.json"
        [String] $jsonFilePath = Join-Path -Path "$jsonOutDir" -ChildPath $fileName

        # Write to file
        Add-content $jsonFilePath -Value ($object | ConvertTo-Json)
    }    
}

# -----------------------------------------------------------------
# Reads Configuration from JSON file
# -----------------------------------------------------------------
Class Config {

    hidden [IO] $io
    hidden $config
    static [String] $CONFIG_FILE = ".\cx_sca_search_config.json"

    # Constructs and loads configuration from given path
    Config () {
        $this.io = [IO]::new()
        $this.LoadConfig()
    }

    # Loads configuration from configured path
    LoadConfig () {
        try {
            $cp = [Config]::CONFIG_FILE
            $configFilePath = (Get-Item -Path $cp).FullName
            $this.io.Log("Loading configuration from $configFilePath")
            $this.config = Get-Content -Path $configFilePath -Raw | ConvertFrom-Json
        }
        catch {
            $this.io.Log("Provided configuration file at [" + [Config]::CONFIG_FILE + "] is missing / corrupt.")        
        }
    }

    [PsCustomObject] GetConfig() {
        return $this.config
    }
}

# -----------------------------------------------------------------
# Credentials Utility
# -----------------------------------------------------------------
Class CredentialsUtil {

    # Returns a PSCredential object from given plaintext username/password
    [PSCredential] GetPSCredential ([String] $username, [String] $plainTextPassword) {
        [SecureString] $secPassword = ConvertTo-SecureString $plainTextPassword -AsPlainText -Force
        return New-Object System.Management.Automation.PSCredential ($username, $secPassword)
    }
}

# -----------------------------------------------------------------
# Database Client
# -----------------------------------------------------------------
Class DBClient {

    hidden [IO] $io = [IO]::new()
    hidden [PSCredential] $sqlAuthCreds
    hidden [String] $serverInstance

    # Constructs a DBClient based on given server and creds
    DBClient ([String] $serverInstance, [String]$dbUser, [String] $dbPass) {
        $this.serverInstance = $serverInstance
        if ($dbUser -and $dbPass) {
            $this.sqlAuthCreds = [CredentialsUtil]::new().GetPSCredential($dbUser, $dbPass)
        }
    }

    # Executes given SQL using either SQLServer authentication or Windows, depending on given PSCredential object
    [PSObject] ExecSQL ([String] $sql, [Hashtable] $parameters) {
        try {
            if ($this.sqlAuthCreds.UserName) {
                $cred = $this.sqlAuthCreds
                return Invoke-Sqlcmd2 -ServerInstance $this.serverInstance -Credential @cred -Query $sql -SqlParameters $parameters -ErrorAction stop
            }
            else {
                return Invoke-Sqlcmd2 -ServerInstance $this.serverInstance -Query $sql -SqlParameters $parameters -ErrorAction stop
            }    
        }
        catch {
            $this.io.Log("Database execution error. $($_.Exception.GetType().FullName), $($_.Exception.Message)")
            # Force exit during dev run - runtime savior
            Exit
        }
    }
}


# -----------------------------------------------------------------
# Teams Utility
# -----------------------------------------------------------------
Class TeamsUtil {

    hidden [IO] $io = [IO]::new()
    hidden [Hashtable] $teamPaths = @{ }
    hidden [Hashtable] $teamNames = @{ }
    hidden [DBClient] $dbClient

    TeamsUtil([DBClient] $dbClient) {
        $this.dbClient = $dbClient
        $teams = $dbClient.ExecSQL("select * from cxdb.dbo.teams", $null)
        if ($teams) {
            foreach ($team in $teams) {
                $this.teamPaths.Add($team["TeamId"], $team["TeamPath"])
                $this.teamNames.Add($team["TeamId"], $team["TeamName"])
            }
        }
    }

    # Generates the full team name from given team ID
    [String] GetFullTeamName ([String] $teamId) {

        [String] $teamPath = $this.teamPaths[$teamId] + $teamId
        
        if ($this.teamPaths -and $this.teamNames) {

            [System.StringSplitOptions] $option = [System.StringSplitOptions]::RemoveEmptyEntries
            $teamPathIds = $teamPath.Split("\\,/", $option)

            foreach ($teamPathId in $teamPathIds) {
                $teamName = $this.teamNames[$teamPathId]
                $teamPath = $teamPath.Replace($teamPathId, $teamName)
            }
        }
        
        return $teamPath
    }
}

# -----------------------------------------------------------------
# SCA Search Utility
# -----------------------------------------------------------------
Class SCASearch {

    hidden [IO] $io
    hidden [DBClient] $dbClient
    hidden [TeamsUtil] $teamsUtil

    # SCA Scan State enumeration
    # NotStarted = 0
    # InProgress = 1
    # Succeeded = 2
    # Failed = 3
    hidden [int32] $scanState = 2

    hidden [String] $searchSql = 
    "SELECT distinct 
        projects.Owning_Team as 'Team',
        projects.Name as 'Project',
        libs.Name as 'Library', libs.Version as 'Version',
        scans.StartAnalyzeTime as 'Found In Scan'
    FROM
        cxdb.dbo.Scans 
		INNER JOIN cxdb.dbo.Projects ON projects.id = scans.projectId 
        INNER JOIN cxdb.dbo.ScannedLibraries scannedlibs ON scans.ScanId = scannedlibs.ScanId 
        INNER JOIN cxdb.dbo.Libraries libs ON libs.Id = scannedlibs.LibraryId 
    WHERE        
        scans.scanState=$($this.scanState) and
        libs.Name like @lib"

    SCASearch ([DBClient] $dbClient) {
        $this.io = [IO]::new()
        $this.dbClient = $dbClient
        $this.teamsUtil = [TeamsUtil]::new($dbClient)
    }

    # Searches for given library name in the Checkmarx SCA results
    Search([String] $lib) {

        # Only supported wildcard is zero-or-more characters.
        [Hashtable] $parameters = @{ "lib" = $lib.Replace("*", "%") }

        [PSObject] $results = $this.dbClient.ExecSQL($this.searchSql, $parameters)
        if ($results) {  
            $this.io.Log("Found [$($results.Count)] results for library '$lib'.")  

            [Array] $nTeams = $results | Select-Object -Unique Team
            [Array] $nProjects = $results | Select-Object -Unique Project
            [Array] $nLibs = $results | Select-Object -Unique Library
            $this.io.Log("Number of Teams that use library : [" + $nTeams.Count + "]")
            $this.io.Log("Number of Projects that use library : [" + $nProjects.Count + "]")
            $this.io.Log("Number of Libraries that matched : [" + $nLibs.Count + "]")
    
            [System.Collections.ArrayList] $resultTable = @()

            foreach ($result in $results) {   

                [String] $scanTime = $result["Found In Scan"]
                [String] $teamName = $this.teamsUtil.GetFullTeamName($result["Team"])
                $result["Team"] = $teamName

                # Create a JSON structure for results
                [PSCustomObject] $resultJSON = [ordered] @{
                    "Team"          = $teamName
                    "Project"       = $result["Project"]
                    "Library"       = $result["Library"]
                    "Version"       = $result["Version"]
                    "Found In Scan" = $scanTime
                }  
                $notUsed = $resultTable.Add($resultJSON)
            }

            if ($script:json) {
                $this.io.Log("Generating JSON from results...")
                $resultTable | ConvertTo-Json | Out-Host
                $this.io.WriteJSON($resultTable)
            }
            else {
                $data = $results | Sort-Object Team, Project
                if ($script:group) {
                    $this.io.Log("Grouping results by [" + $script:group + "]")
                    $data | Format-Table -AutoSize -GroupBy $script:group | Out-Host
                }
                else {
                    if ($script:grid) {
                        $data | Out-GridView -Title "Checkmarx SCA Search Results - [$lib]"            
                    }
                    else {
                        $data | Format-Table -AutoSize | Out-Host
                    }
                }
            }
        }
        else {
            $this.io.Console("No libraries matched '$lib'.")      
        }
    }
}

# -----------------------------------------------------------------
# -----------------------------------------------------------------
#
# Execution entry
#
# -----------------------------------------------------------------
# -----------------------------------------------------------------

# Check if PS v5+
$psv = $PSVersionTable.PSVersion.Major
if ($psv -and $psv -lt 5) {
    Write-Host "Requires PSv5 and greater."
    Exit
}

# Load configuration
[PSCustomObject] $config = [Config]::new().GetConfig()
# Override if values were explicitly overridden via the commandline
if ($dbUser) { $config.cx.db.username = $dbUser }
if ($dbPass) { $config.cx.db.password = $dbPass }


# Create an IO utility object
[IO] $io = [IO]::new()

# Create a DB Client
[DBClient] $dbClient = [DBClient]::new($config.cx.db.instance, $config.cx.db.username, $config.cx.db.password)

# Spit out pretty headers
$io.WriteHeader()

# Force TLS1.2
[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12

# SCASearch
[SCASearch] $scaSearch = [SCASearch]::new($dbClient)

$scaSearch.Search($lib)