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
$team_index = New-Object 'System.Collections.Generic.Dictionary[string,string]'
$teams | % { 
    $team_index.Add($_.id, $_.fullName)
    Write-Debug $_ 
} 

Write-Output "Scans section starting"

$report_index = New-Object 'System.Collections.Generic.Dictionary[string,string]'
$scan_index = New-Object 'System.Collections.Generic.Dictionary[string,string]'
$prj_index = New-Object 'System.Collections.Generic.Dictionary[string,string]'

$projects | % {
    
    $scans = &"support/rest/sast/scans.ps1" $session $_.id
    $scan_index.Add($scans.id, $scans.owningTeamId)
    $prj_index.Add($scans.id, $scans.project.name)
    
    Write-Output $scans

    #generate the report
    $report = &"support/soap/generate_report.ps1" $session $scans.id
    $report_index.Add($scans.id, $report)

}

#Probe for report completion
Write-Output "Checking status of all reports"
$report_index.Keys |%{
    $reportId = $report_index.Item($_)
    $reportstatus = &"support/rest/sast/reportStatus.ps1" $session $reportId
    
    while ($reportstatus.status.value -ne "Created" -and $reportstatus.status.value -ne "Failed") {
        $reportstatus = &"support/rest/sast/reportStatus.ps1" $session $reportId
        Write-Debug $reportstatus.status.value
    }
    if($reportstatus.status.value -eq "Created"){
        $status = [String]::Format("Report successfully created for id = {0}", $reportId)
    }else{
        $status = [String]::Format("Report creation failed for id = {0}", $reportId)
    }
    Write-Output $status
}

Write-Output "All reports have been created"

#Download all reports
Write-Output "Starting to download all reports"
$report_index.Keys | %{
    #get all team, project, scan, report, and output path information
    $reportid = $report_index.Item($_)
    $scanid = $report_index.Item($_)
    $teamid = $scan_index.Item($_)
    $teamName = $team_index.Item($teamid)
    $projectName = $prj_index.Item($_)
    $outputPath = $PSScriptRoot + "\Output"

    Write-Debug "ScanId = $scanid , team name = $teamName, project name = $projectName, reportId = $reportid"
    Write-Output "Downloading report for $teamName\$projectName"


    &"support/rest/sast/getreport.ps1" $session $reportid $teamName $projectName $outputPath

}
