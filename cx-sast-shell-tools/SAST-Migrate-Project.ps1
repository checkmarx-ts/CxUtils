param(
    [Parameter(Mandatory = $true)]
    [System.Uri]$old_sast_url,
    [Parameter(Mandatory = $true)]
    [System.Uri]$new_sast_url,

    [Parameter(Mandatory = $true)]
    [String]$old_sast_username,
    [Parameter(Mandatory = $true)]
    [String]$new_sast_username,

    [Parameter(Mandatory = $true)]
    [String]$old_sast_password,
    [Parameter(Mandatory = $true)]
    [String]$new_sast_password,

    [Parameter(Mandatory = $true)]
    [String]$old_sast_team_path,
    [Parameter(Mandatory = $true)]
    [String]$new_sast_team_path,

    [Parameter(Mandatory = $true)]
    [String]$project_name,

    [String]$new_preset_name,
    [String]$new_config_name,

    [Switch]$dbg
)

. "support/debug.ps1"

setupDebug($dbg.IsPresent)


function GetTeamId
{
    param($team_path, $team_json)

    $result = $null
    $team_json | % { 

        if ($_.fullName.CompareTo($team_path) -eq 0) {
            $result = $_.id
            Write-Debug "Matched: $result"
            return $result
        }
        elseif ($dbg.IsPresent) {
            Write-Debug "$($_.fullName) != $team_path"
        }
    }
}


Write-Output "Logging in as $old_sast_username to $old_sast_url"
$old_session = &"support/rest/sast/login.ps1" $old_sast_url $old_sast_username $old_sast_password -dbg:$dbg.IsPresent

Write-Output "Logging in as $new_sast_username to $new_sast_url"
$new_session = &"support/rest/sast/login.ps1" $new_sast_url $new_sast_username $new_sast_password -dbg:$dbg.IsPresent


$timer = $(Get-Date)
Write-Output "Fetching teams from $old_sast_url"
$teams = &"support/rest/sast/teams.ps1" $old_session
Write-Output "$($teams.Length) teams fetched - elapsed time $($(Get-Date).Subtract($timer))"
$old_team_id = GetTeamId $old_sast_team_path $teams

if ($null -eq $old_team_id) {
    throw "The old project team could not be found."
}
else {
    Write-Output "Old team id: $old_team_id"
}

$timer = $(Get-Date)
Write-Output "Fetching teams from $new_sast_url"
$teams = &"support/rest/sast/teams.ps1" $new_session
Write-Output "$($teams.Length) teams fetched - elapsed time $($(Get-Date).Subtract($timer))"
$new_team_id = GetTeamId $new_sast_team_path $teams

if ($null -eq $new_team_id) {
    throw "The new project team could not be found."
}
else {
    Write-Output "New team id: $new_team_id"
}


$timer = $(Get-Date)
Write-Output "Fetching projects from $old_sast_url"
$project_list = &"support/rest/sast/projects.ps1" $old_session
Write-Output "$($project_list.Length) projects fetched - elapsed time $($(Get-Date).Subtract($timer))"
$old_project = $null

$project_list | %{

    if ($_.teamId.CompareTo($old_team_id) -eq 0) {
        if ($_.name.CompareTo($project_name) -eq 0) {
            $old_project = $_
            return
        }
    }
}

if ($null -eq $old_project) {
    throw "The project to migrate could not be found."
}



# BEFORE CREATING THE PROJECT, VALIDATE:
# defined or existing preset exists (name match)
# defined or existing engine config exists (name match)
# custom fields in the old project exist in the new project

$old_scan_settings = $null

$old_project.links | %{

    if ($_.rel.CompareTo("scansettings") -eq 0)
    {
        $old_scan_settings = &"support/rest/sast/scanSettings" $old_session $_.uri

    }
}

if ($null -eq $old_scan_settings) {
    throw "Could not retreive scan settings for $($old_project.name)"
}


# MAP PRESET HERE
$new_preset = $old_scan_settings.preset.id

# MAP ENGINE CONFIG HERE
$new_engine_config = $old_scan_settings.engineConfiguration.id






$timer = $(Get-Date)
Write-Output "Fetching projects from $new_sast_url"
$project_list = &"support/rest/sast/projects.ps1" $new_session
Write-Output "$($project_list.Length) projects fetched - elapsed time $($(Get-Date).Subtract($timer))"
$new_project = $null

$project_list | %{

    if ($_.teamId.CompareTo($new_team_id) -eq 0) {
        if ($_.name.CompareTo($project_name) -eq 0) {
            $new_project = $_
            return
        }
    }
}

if ($null -eq $new_project) {
    # Create the new project with default settings
    Write-Output "$project_name does not exist in team $new_sast_team_path on $new_sast_url, creating."
    $new_project = &"support/rest/sast/create/projects.ps1" $new_session $project_name $new_team_id
}


Write-Output "New project id: $($new_project.id)"



&"support/rest/sast/update/scanSettings.ps1" $new_session $new_project.id $new_preset $new_engine_config `
    $old_scan_settings.emailNotifications.failedScan `
    $old_scan_settings.emailNotifications.beforeScan `
    $old_scan_settings.emailNotifications.afterScan 


#TBD: Issue tracking settings
#TBD: Custom fields
#TBD: Data Retention
#TBD: Exclude files/folders


# not going to set location data, scheduling, issue tracking, OSA, post scan action


