<#

    .SYNOPSIS
        Used to migrate project configurations from one instance of CxSAST to a new instance of CxSAST.

    .DESCRIPTION
        This is intended to be used to migrate projects that are configured with a "Local" source location.  Given the scope
        of this script, the following limitations apply:

        * Location data is not migrated (migrated projects default to "Local" source location)
        * Scheduling configurations are not migrated (it is not possible to schedule scans for "Local" source location)
        * Issue tracking settings are not migrated
        * Post scan actions are not migrated
        * OSA settings are not migrated
        * Policy settings are not migrated
        * Data retention settings are not migrated
        * Preset selections are migrated, but there is no verification that the presets between the two systems are equivalent
        * The user accounts can not be SSO accounts since there is no interactive login component for the API

        Example 1 shows migrating projects from an 8.9 instance to a 9.x instance.  Note the team path separator changed between 8.9 and 9.x.
        Example 2 shows migrating projects between 9.x instances.

    .PARAMETER old_sast_url
        The URL to the old CxSAST instance where the project is currently defined.

    .PARAMETER new_sast_url
        The URL to the new CxSAST instance where the migrated project will be created.

    .PARAMETER old_sast_username
        The name of the user in the old CxSAST system that will be used to read the migrating project definition.

    .PARAMETER new_sast_username
        The name of the user in the new CxSAST system that will be used to create the new project definition.

    .PARAMETER old_sast_password
        The password for the user in the old CxSAST system.


    .PARAMETER new_sast_password
        The password for the user in the new CxSAST system.

    .PARAMETER old_sast_team_path
        The team path in the old system where the project to be migrated is assigned.
    
    .PARAMETER new_sast_team_path
        The team path in the new system where the migrated project definition will be created.

    .PARAMETER project_name
        The name of the project to migrate from the old system to the new system.

    .PARAMETER new_preset_name
        (Optional) The preset definition to use in the new system.  If not provided, the chosen preset definition of the original project is used
        if it exists in the new system.  If there is a mismatch in the name of the preset for the preset id used in the old system, 
        the script will end in error.

    .PARAMETER new_engine_config_name
        (Optional) The engine configuration to use in the new system.  If not provided, the engine configuration of the original project is used
        if it exists in the new system.  If there is a mismatch in the engine configuration name, the script will end in error.

    .PARAMETER dbg
        (Optional Flag) Runs in debug mode and prints verbose information to the screen while processing. 

    .INPUTS
        None

    .OUTPUTS
        None

    .EXAMPLE
        .\SAST-Migrate-Project.ps1 `
        -old_sast_url http://sast89.company.com `
        -old_sast_username ... `
        -old_sast_password ... `
        -new_sast_url http://sast9x.company.com `
        -new_sast_username ... `
        -new_sast_password ... `
        -old_sast_team_path "\CxServer\SP\Company\Users" `
        -new_sast_team_path /CxServer/ThisIsASubTeam `
        -project_name "My Project"

    .EXAMPLE 

        .\SAST-Migrate-Project.ps1 `
        -old_sast_url http://old.system.company.com `
        -old_sast_username ... `
        -old_sast_password ... `
        -new_sast_url http://new.system.company.com `
        -new_sast_username ... `
        -new_sast_password ... `
        -old_sast_team_path "/CxServer/MyTeam" `
        -new_sast_team_path /CxServer/Organization/MyTeam `
        -project_name "My Project"

#>
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
    [String]$new_engine_config_name,

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



function GetConfigIdFromList{
    param ($script_path,$pname,$new_name,$old_id)

    if ([String]::IsNullOrEmpty($new_name) -ne $true) {
        Write-Debug "New $pname name $new_name specified"
    
        # Find config in new system by name
        $list = &"$script_path" $new_session
    
        $found = $null
    
        $list | %{
    
            if ($_.name.CompareTo($new_name) -eq 0) {
                $found = $_.id
                return
            }
        }
    
        if ($found -eq $null) {
            throw "Unable to find a $pname named $new_name at $new_sast_url"
        }
        else {
            Write-Debug "New $pname name $new_name found with id: $found"
            return $found
        }
    }
    else {
        # Using config id, check the names between new and old system are the same
        Write-Debug "Attempting to use existing $pname"
    
        $old_list = &$script_path $old_session
        $new_list = &$script_path $new_session
    
        $old_name = $null
        $old_list | %{
            if ($_.id -eq $old_id) {
                $old_name = $_.name
                return
            }
        }
    
        if ($old_name -eq $null) {
            throw "Unable to find the name of the $pname id $old_id at $old_sast_url"
        }
    
        Write-Debug "Existing project $pname $($old_id):$old_name"
   
        $result = $null

        $new_list | %{
            if ($_.id -eq $old_id) {
                if ($_.name.CompareTo($old_name) -eq 0) {
                    Write-Debug "Matched existing $pname in the new system"
                    $result = $_.id
                    return
                }
                else {
                    throw "Old preset $($old_id):$old_name does not match preset $($_.id):$($_.name)."
                }
            }
        }
    
        if ($result -eq $null) {
            throw "Could not find a $pname matching $($old_id):$old_name in $new_sast_url"
        }

        return $result
    }    
}

$new_preset = GetConfigIdFromList "support/rest/sast/presets.ps1" "preset" $new_preset_name $old_scan_settings.preset.id
$new_engine_config = GetConfigIdFromList "support/rest/sast/engineConfigurations.ps1" "engine config" $new_engine_config_name `
    $old_scan_settings.engineConfiguration.id

# Validate custom fields
$old_project_config = &"support/rest/sast/projects.ps1" $old_session $old_scan_settings.project.id

$custom_fields_to_update = New-Object 'System.Collections.Generic.List[PSCustomObject]'

if ($old_project_config.customFields.length -ne 0) {
    Write-Debug "Found $($old_project_config.customFields.length) custom fields defined in the old project"
    
    $old_fields_dict = New-Object 'System.Collections.Generic.Dictionary[String, PSCustomObject]'

    $old_project_config.customFields | %{
        $old_fields_dict.Add($_.name, $_)
    }

    $new_system_fields = &"support/rest/sast/customFields.ps1" $new_session

    $new_system_fields_map = New-Object 'System.Collections.Generic.Dictionary[String, PSCustomObject]'

    $new_system_fields | %{
        $new_system_fields_map.Add($_.name, $_)
    }


    $old_fields_dict.Keys | %{

        if ($new_system_fields_map.ContainsKey($_) -ne $true)
        {
            throw "Custom field $_ is not defined in $new_sast_url"
        }
        else {
            $custom_fields_to_update.Add(@{
                id = $new_system_fields_map[$_].id
                value = $old_fields_dict[$_].value
            })
        }
    }
}

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
    $old_scan_settings.emailNotifications.afterScan | Out-Null

if ($custom_fields_to_update.Count -ne 0) {

    $update_payload = [ordered]@{
        name = $project_name
        owningTeam = $new_team_id
        customFields = $custom_fields_to_update
    }

    &"support/rest/sast/update/projects.ps1" $new_session $new_project.id $update_payload
}

$old_exclude_settings = &"support/rest/sast/excludeSettings.ps1" $old_session $old_scan_settings.project.id

&"support/rest/sast/update/excludeSettings.ps1" $new_session $new_project.id `
    @{
        excludeFoldersPattern = $old_exclude_settings.excludeFoldersPattern
        excludeFilesPattern = $old_exclude_settings.excludeFilesPattern
    } | Out-Null



