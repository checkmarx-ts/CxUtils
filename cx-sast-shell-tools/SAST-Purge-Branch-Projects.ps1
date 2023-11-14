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

    .PARAMETER page_size
        Defaults to 25.  Sets the limit of the number of projects retrieved with each call to the OData API.

    .PARAMETER latest_scan_days
        (Optional) Specifies the maximum number of days old the latest scan should be before
        selecting the branch project for purge.

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
    [int]$page_size=25,
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

$max_date = [System.DateTime]::Now.AddDays(-1 * $latest_scan_days)
$session = &"$PSScriptRoot/support/rest/sast/login.ps1" $sast_url $username $password -dbg:$dbg.IsPresent


function RetrieveProjects() {

  $after_project = $null
  $result = @()
  $selected = 0

  do
  {
    $page = &"$PSScriptRoot/support/odata/GetProjectListByPage.ps1" $session $page_size $after_project


    if ($null -ne $page -and $null -ne $page.value -and $page.value.Length -gt 0) {
        $after_project = $page.value[$page.value.Length - 1].Id
        foreach ($_ in $page.value) {

            $last_scan = $_.LastScan

            if ($null -ne $last_scan -and $null -ne $last_scan.ScanCompletedOn) {

                $last_scan_date = [System.DateTime]::Parse($last_scan.ScanCompletedOn)

                if ($last_scan_date.CompareTo($max_date) -ge 0) {
                   continue   
                }
            }

            if ($limit -ne 0 -and $selected -eq $limit) {
              break
            }

            $project = &"$PSScriptRoot/support/rest/sast/projects.ps1" $session $_.Id "2.2"

            if ($null -ne $project -and $project.isBranched -eq $true) {
              $result += $_
              $selected += 1
            }
        }
    }


  } while ( $null -ne $page -and $null -ne $page.value -and $page.value.Length -eq $page_size -and -not ($limit -ne 0 -and $selected -eq $limit) )


  return $result
}


Write-Output "Retrieving branch projects..."
$data = RetrieveProjects

if ($null -eq $data -or ($null -ne $data -and $data.Length -eq 0) ) {
    Write-Output "No branch projects selected for delete."
    exit 1
}


Write-Output "Retrieving teams..."
$teams = IndexTeams (&"$PSScriptRoot/support/rest/sast/teams.ps1" -session $session)

$prefix = ""
if ($commit) {$prefix = "DELETE: "}

foreach ($_ in $data) {

    $cur_proj = "$($prefix)Branch Project Id $($_.Id): $($teams[$_.OwningTeamId])/$($_.Name)"
    Write-Host $cur_proj

    if ($commit) {
        &"$PSScriptRoot/support/rest/sast/delete/projects.ps1" -session $session -project_id $_.Id | Out-Null
    }

}
