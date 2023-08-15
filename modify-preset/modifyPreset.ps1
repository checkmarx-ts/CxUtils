<#
.Synopsis
Used to update a exisiting preset with a new one across all projects

.Description
This script will produce a report of the Scan settings for all projects as a 
CSV file or to update a selected preset to the new preset across all projects.

The script prompts for a CxSAST username and password. If your environment does not have GUI support then you should first enable console prompting.

    $key = "HKLM:\SOFTWARE\Microsoft\PowerShell\1\ShellIds"
    Set-ItemProperty $key ConsolePrompting True

Usage
Help
    .\Desktop\ModifyPreset.ps1 [-help] [<CommonParameters>]
    
Reporting
    .\ModifyPreset.ps1 [-filePath <String>] -baseURI <String> [-teamNameFilter <String[]>] [<CommonParameters>]
    .\ModifyPreset.ps1 [-filePath <String>] -baseURI <String> [-teamIdFilter <Int32[]>] [<CommonParameters>]    

Update   
    .\ModifyPreset.ps1 [-update] -baseURI <String> [-teamIdFilter <Int32[]>] -currentPreset <String> -newPreset <String> [<CommonParameters>]  
    .\ModifyPreset.ps1 [-update] -baseURI <String> [-teamNameFilter <String[]>] -currentPreset <String> -newPreset <String> [<CommonParameters>]

.Notes
Version:     3.0
Date:        28/07/2023
Written by:  Michael Fowler
Contact:     michael.fowler@checkmarx.com

Change Log
Version    Detail
-----------------
1.0        Original version
2.0        Removed username and password parameters and replaced with credentials
           Added Team filters to filter results by arrays of Team IDs or Team Names  
3.0        Added logic to handle additional values introduced in API v4 and stop these being overridden
  
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
#>

#------------------------------------------------------------------------------------------------------------------------------------------
# Parameters
[CmdletBinding(DefaultParameterSetName='Report')]
Param(
    [Parameter(ParameterSetName='Help',Mandatory=$false, HelpMessage="Display help")]
    [switch]$help,
    
    [Parameter(ParameterSetName='Update',Mandatory=$false, HelpMessage="Update presets")]
    [switch]$update,
    
    [Parameter(ParameterSetName='Report',Mandatory=$false, HelpMessage="Enter Full path for the report")]
    [string]$filePath = "$PSScriptRoot\Scan Settings Report.csv", 

    [Parameter(ParameterSetName='Update',Mandatory=$true, HelpMessage="SAST URL")]
    [Parameter(ParameterSetName='Report',Mandatory=$true, HelpMessage="SAST URL")]
    [string]$baseURI,

    [Parameter(ParameterSetName='Update',Mandatory=$false, HelpMessage="Comma seperated list of Team Names to filter by")]
    [Parameter(ParameterSetName='Report',Mandatory=$false, HelpMessage="Comma seperated list of Team Names to filter by")]
    [string[]]$teamNameFilter=@(),

    [Parameter(ParameterSetName='Update',Mandatory=$false, HelpMessage="Comma seperated list of Team IDs to filter by")]
    [Parameter(ParameterSetName='Report',Mandatory=$false, HelpMessage="Comma seperated list of Team ID to filter by")]
    [int[]]$teamIdFilter=@(),

    [Parameter(ParameterSetName='Update',Mandatory=$true, HelpMessage="Preset to be updated")]
    [string]$currentPreset,
     
    [Parameter(ParameterSetName='Update',Mandatory=$true, HelpMessage="Preset to change to")]
    [string]$newPreset
)

#------------------------------------------------------------------------------------------------------------------------------------------
#Project Class

class Project {
    [string]$ProjectName
    [string]$ProjectId
    [string]$TeamId
    [string]$TeamName
    [string]$PresetName
    [string]$PresetId
    [string]$EngineConfigurationId
    [string]$PostScanActionName
    [string]$PostScanActionId
    [array]$EmailFailedScan
    [array]$EmailBeforeScan
    [array]$EmailAfterScan

    #Used for v4 API only
    [string]$RunOnlyWhenNewResults
    [string]$RunOnlyWhenNewResultsMinSeverity
    [string]$PostScanActionArguments
}

#------------------------------------------------------------------------------------------------------------------------------------------
# Login and create header

Function private:CreateHeader {
    Write-Verbose "Starting Authentication"   
    
    $cred = $host.ui.PromptForCredential("Checkmarx Credentials", "Please enter your SAST user name and password.", $null, $null)   
    if ($cred -eq $null) {
        throw "Checkmarx username and password not entered"
    }
    
    #Get Access token
    $uri = $baseURI + "/cxrestapi/auth/identity/connect/token"
    $body = @{
        username = $cred.UserName
        password = $cred.GetNetworkCredential().password
        grant_type = "password"
        scope = "access_control_api sast_rest_api"
        client_id = "resource_owner_client"
        client_secret = "014DF517-39D1-4453-B7B3-9930C563627C"
    }
    try {
        $access_token = (Invoke-RestMethod -Uri $uri -Method POST -Body $body).access_token
    }
    catch {
        Write-Error "Error authenticating. Please check the URI, Username and Password and try again"
        exit
    }

    Write-Verbose "Authentication Completed"
    
    return @{
        accept = "application/json"
        Authorization = "Bearer $access_token"
    }
}

#------------------------------------------------------------------------------------------------------------------------------------------
# Get functions to get project data

#Get presets
Function private:GetPresets {
    param (
        [HashTable]$header
    )

    Write-Verbose "Getting Presets"
    
    $uri = $baseURI + "/cxrestapi/help/sast/presets"
    $presets = Invoke-RestMethod -Uri $uri -Method GET -Headers $header
 
    $presetsHash = @{}
    foreach ($i in $presets) {
        $presetsHash.Add($i.id, $i.name)
        if ($i.name -eq $newPreset) { $newPresetId = $i.id }
    }

    Write-Verbose "$($Presets.Count) Presets returned"
    return $presetsHash, $newPresetId
}

#Get Teams
Function private:GetTeams {

    param (
        [HashTable]$header
    )

    Write-Verbose "Getting Teams"

    $uri = $baseURI + "/cxrestapi/auth/Teams"
    $teams = Invoke-RestMethod -Uri $uri -Method GET -Headers $header

    $teamssHash = @{}
    foreach ($i in $teams) {
        $teamssHash.Add($i.id, $i.name)
    }

    Write-Verbose  "$($Teams.Count) Teams returned"
    return $teamssHash
}

#Get all projects and store Project ID, Project name and Project Owner
Function private:GetProjects {
    param (
        [HashTable]$header, 
        [System.Object]$projectsList,
        [HashTable]$teams
    )
    
    Write-Verbose "Getting Projects"

    $projectsList = New-Object System.Collections.Generic.List[System.Object]
    $uri = $baseURI + "/cxrestapi/help/projects"
    
    try {
        $projects = Invoke-RestMethod -Uri $uri -Method GET -Headers $header
    }
    catch {
        Write-Error "Error retrieving projects. Please check the user selected has the appropiate rights for this command"
        exit
    }

    # Add projects to list if filters not used, team name is in the name filter or team Id is in the Id filter
    foreach ($i in $projects) {
        if (
                (-not $teamNameFilter -and -not $teamIdFilter) -or
                ($teamNameFilter -and ($teams[$i.teamId] -in $teamNameFilter)) -or
                ($teamIdFilter -and ($i.teamId -in $teamIdFilter))
            ) {
            $p = [Project]::new()
            $p.ProjectName = $i.name
            $p.ProjectId = $i.id
            $p.TeamId = $i.teamId
            $p.TeamName = $teams[$i.teamId]
            $projectsList.Add($p)
        }
    }

    Write-Verbose "$($projects.Count) Projects returned"
    return $projectsList
}

# Get Project scan settings
Function private:GetProjectScanSettings {
    param (
        [HashTable]$header, 
        [System.Object]$projects, 
        [HashTable]$presets
    )

    Write-Verbose "Getting Scan Settings"
    $v4 = $false

    foreach ($p in $projects) {
        $uri = $baseURI + "/cxrestapi/help/sast/scanSettings/" + $p.ProjectId
        $scanSttings = Invoke-RestMethod -Uri $uri -Method GET -Headers $header
 
        $p.PresetId = $scanSttings.preset.id
        $p.PresetName = $presets[$scanSttings.preset.id]
        $p.EngineConfigurationId = $scanSttings.engineConfiguration.id  
        $p.PostScanActionName = $scanSttings.postScanActionName
        $p.PostScanActionId = $scanSttings.postScanAction.id   
        $p.EmailFailedScan = $scanSttings.emailNotifications.failedScan
        $p.EmailBeforeScan = $scanSttings.emailNotifications.beforeScan
        $p.EmailAfterScan = $scanSttings.emailNotifications.afterScan

        if ($scanSttings.postScanActionConditions) {
            if (-NOT $v4) { $v4 = $true }
            $p.RunOnlyWhenNewResults = $scanSttings.postScanActionConditions.runOnlyWhenNewResults
            $p.RunOnlyWhenNewResultsMinSeverity = $scanSttings.postScanActionConditions.runOnlyWhenNewResultsMinSeverity
            $p.PostScanActionArguments = $scanSttings.postScanActionArguments
        }
    }


    Write-Verbose "Scan Settings returned"
    return $v4
}

#------------------------------------------------------------------------------------------------------------------------------------------
#Update and Report functions

Function private:CreateProjectsReport {
    param (
        [System.Object]$projects,
        [string]$filePath
    )

    Write-Verbose "Creating projects report"

    $projectOutput = $projects | ForEach-Object {       
        [PSCustomObject]@{
            "Project Name" = $_.ProjectName
            "Project ID" = $_.ProjectId
            "Team Name" = $_.TeamName
            "Team ID" = $_.TeamId
            "Preset Name" = $_.PresetName
            "Preset ID" = $_.PresetId
            "Engine Configuration ID" = $_.EngineConfigurationId
            "Post Scan Action Name" = $_.PostScanActionName
            "Post Scan Action ID" = $_.PostScanActionId
            "Email Failed Scan" = ($_.EmailFailedScan) -join ';'
            "Email Before Scan" = ($_.EmailBeforeScan) -join ';'
            "Email After Scan" = ($_.EmailAfterScan) -join ';'
            "Run Only When New Results (v4 API)" = $_.RunOnlyWhenNewResults
            "Run Only When New Results Min Severity (v4 API)" = $_.RunOnlyWhenNewResultsMinSeverity
            "Post Scan Action Arguments (v4 API)" = $_.PostScanActionArguments
        }
    }
    $projectOutput | Export-Csv -Path $filepath -NoTypeInformation
}

#Update presets using new value
Function private:UpdateProjectPreset {
    param (
        [HashTable]$header, 
        [System.Object]$projects, 
        [HashTable]$presets, 
        [Int64]$newPresetId,
        [bool]$v4
    )

    Write-Verbose "Updating projects"

    $updateCount = 0

    foreach ($p in $projects) {
        if ($p.PresetName -eq $currentPreset.Trim('''"')) {
            $uri = $baseURI + "/cxrestapi/help/sast/scanSettings"    
            $body = @{
                "projectId" = $p.ProjectId
                "presetId" = $newPresetId
                "engineConfigurationId" = $p.EngineConfigurationId
                "postScanActionId" = $p.postScanActionId
                "emailNotifications"= @{
                    "failedScan" = $p.EmailFailedScan
                    "beforeScan" = $p.EmailBeforeScan
                    "afterScan" = $p.EmailAfterScan
                }
            } 
            if ($v4) {
                $body.Add("postScanActionConditions", @{
                    "runOnlyWhenNewResults" = $p.RunOnlyWhenNewResults
                    "runOnlyWhenNewResultsMinSeverity" = $p.RunOnlyWhenNewResultsMinSeverity
                })
                $body.Add("postScanActionArguments", $p.PostScanActionArguments)
            }

            $return = Invoke-RestMethod -Uri $uri -Method PUT -Headers $header -Body ($body | ConvertTo-Json) -ContentType "application/json"
            
            Write-Verbose "Project $($p.ProjectName) projectName preset updated to $newPreset"
            $updateCount++
        }
    }
    
    return $updateCount
}

#------------------------------------------------------------------------------------------------------------------------------------------
# Main

if ($teamNameFilter -and $teamIdFilter) {
    throw "Use either Team Name or Team ID as filter."
}

if ($help) {
    Get-Help $MyInvocation.InvocationName -Full | Out-String
    return
}

Write-Output "`nProcessing Started"

$header = CreateHeader
$presets, $newPresetId = GetPresets $header
$teams = GetTeams $header
$projects = GetProjects $header $projects $teams
$v4 = GetProjectScanSettings $header $projects $presets
if ($update) {
    $updateCount = UpdateProjectPreset $header $projects $presets $newPresetId $v4
    Write-Output "$updateCount projects updated"
}
else {
    CreateProjectsReport $projects $filePath
    Write-Output "Report written to $filePath"
}

Write-Output "Processing Completed"