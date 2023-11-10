<#

    .SYNOPSIS
        This script finds projects that have no scans, then optionally deletes the projects.


    .DESCRIPTION

    The script enumerates projects in the system, then queries for the latest scan in each project.  If no
    scan is found the project is considered for deletion.
    
    .PARAMETER sast_url
        The URL to the CxSAST instance.

    .PARAMETER username
        The name of the user in the CxSAST system.

    .PARAMETER password
        The password for the user in the CxSAST system.

    .PARAMETER commit
        If included, deletes the projects found that have no scans.
        
    .PARAMETER limit
        Defaults to 0.  Sets the limit of the number of projects to delete.

    .PARAMETER dbg
        (Optional Flag) Runs in debug mode and prints verbose information to the screen while processing. 

    .INPUTS
    None

    .OUTPUTS
    A list of scans proposed for deletion if run without -commit.
    A list of scans deleted if run with -commit.

#>
param(
    [Parameter(Mandatory = $true)]
    [System.Uri]$sast_url,
    [Parameter(Mandatory = $true)]
    [String]$username,
    [Parameter(Mandatory = $true)]
    [String]$password,
    [Switch]$commit,
    [int]$limit=0,
    [Switch]$dbg
)

. "$PSScriptRoot/support/debug.ps1"

setupDebug($dbg.IsPresent)



function IndexTeams
{
    param($team_resp)

    $dict = New-Object System.Collections.Generic.Dictionary"[Int,String]"

    $team_resp | ForEach-Object { 
        $dict.Add($_.Id, $_.fullName)
    }

    return $dict
}



$session = &"$PSScriptRoot/support/rest/sast/login.ps1" $sast_url $username $password -dbg:$dbg.IsPresent

$data = &"$PSScriptRoot/support/odata/GetScanCountByProject.ps1" -session $session

$teams = IndexTeams (&"$PSScriptRoot/support/rest/sast/teams.ps1" -session $session)

$count = 0

$prefix = ""
if ($commit) {$prefix = "DELETE: "}

foreach ($_ in $data[1].value) {
    if ($limit -eq 0 -or $count -lt $limit) {
        $cur_proj = "$($prefix)Project Id $($_.Id): $($teams[$_.OwningTeamId])/$($_.Name)"
        Write-Host $cur_proj
        if ($commit) {
            &"$PSScriptRoot/support/rest/sast/delete/projects.ps1" -session $session -project_id $_.Id | Out-Null
        }
    }
    else { 
        break
    }

    $count = $count + 1
}


