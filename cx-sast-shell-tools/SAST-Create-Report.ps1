param(
    [Parameter(Mandatory = $true)]
    [System.Uri]$sast_url,
    [Parameter(Mandatory = $true)]
    [String]$username,
    [Parameter(Mandatory = $true)]
    [String]$password,
    [Switch]$dbg
)

. "support/debug.ps1"

setupDebug($dbg.IsPresent)


# login
# use rest api to
# - Get projects
# - Get the last finished scan for each project
# Use soap api to create a report with the template
# Use rest api to
# - probe for report complete
# - download report

$session = &"support/rest/sast/login.ps1" $sast_url $username $password -dbg:$dbg.IsPresent

$timer = $(Get-Date)
Write-Output "Fetching projects"
$projects = &"support/rest/sast/projects.ps1" $session
Write-Output "$($projects.Length) projects fetched - elapsed time $($(Get-Date).Subtract($timer))"
$projects | % { Write-Debug $_ } 

# refresh login, if needed
$session = &"support/rest/sast/login.ps1" -existing_session $session -dbg:$dbg.IsPresent


$timer = $(Get-Date)
Write-Output "Fetching teams"
$teams = &"support/rest/sast/teams.ps1" $session
Write-Output "$($teams.Length) teams fetched - elapsed time $($(Get-Date).Subtract($timer))"
$team_index = New-Object 'System.Collections.Generic.Dictionary[int,string]'
$teams | % { 
    $team_index.Add($_.id, $_.fullName)
    Write-Debug $_ 
} 


$projects | % {
    $scan = &"support/rest/sast/scans.ps1" $session $_.id
    # TODO: response can be null for no scans.
    # $_.name
    # $_.teamId
    Write-Output $scan
}