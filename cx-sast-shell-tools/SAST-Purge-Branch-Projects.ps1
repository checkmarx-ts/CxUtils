<#
    .SYNOPSIS
        This script projects that are for branches off the default branch and purges them based on criteria.

    .DESCRIPTION

    The script enumerates projects in the system, then selects only projects that are branched.  All branch projects
    are selected for purge by default. Some optional criteria can be supplied to remove the project from the set of projects
    to be purged.
    
    .PARAMETER sast_url
        The URL to the CxSAST instance.

    .PARAMETER username
        The name of the user in the CxSAST system.

    .PARAMETER password
        The password for the user in the CxSAST system.

    .PARAMETER commit
        If included, performs the delete.
        
    .PARAMETER limit
        Defaults to 0.  Sets the limit of the number of projects to delete.

    .PARAMETER latest_scan_days
        (Optional) Specifies the maximum number of days old the latest scan should be before
        selecting the branch project for purge.  This will make the script take a long time to execute.

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
    [int]$latest_scan_days=0,
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


function FilterForBranchProjects($project_array)
{
    $result = @()

    foreach ($_ in $project_array) {

        if ($_.isBranched) {
            $result += $_
        }
    }

    return $result
}


$session = &"$PSScriptRoot/support/rest/sast/login.ps1" $sast_url $username $password -dbg:$dbg.IsPresent

Write-Output "Retrieving branch projects..."
$data = FilterForBranchProjects (&"$PSScriptRoot/support/rest/sast/projects.ps1" -session $session -api_version "2.2")

Write-Output "Retrieving teams..."
$teams = IndexTeams (&"$PSScriptRoot/support/rest/sast/teams.ps1" -session $session)

$max_date = [System.DateTime]::Now.AddDays(-1 * $latest_scan_days)


$count = 0

$prefix = ""
if ($commit) {$prefix = "DELETE: "}

foreach ($_ in $data) {
    if ($limit -eq 0 -or $count -lt $limit) {

        if ($latest_scan_days -gt 0) {
            $last_scan = &"$PSScriptRoot/support/rest/sast/scans.ps1" -session $session -projectId $_.id

            if ($null -ne $last_scan -and $null -ne $last_scan.dateAndTime -and $null -ne $last_scan.dateAndTime.finishedOn) {

                $last_scan_date = [System.DateTime]::Parse($last_scan.dateAndTime.finishedOn)

                if ($last_scan_date.CompareTo($max_date) -ge 0) {
                   continue   
                }
            }
        }


        $cur_proj = "$($prefix)Project Id $($_.Id): $($teams[$_.teamId])/$($_.Name)"
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


