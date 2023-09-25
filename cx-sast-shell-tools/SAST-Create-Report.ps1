<#

    .SYNOPSIS
        This script iterates projects in the SAST system and generates reports for each scan using a user-defined template.

    .DESCRIPTION
        The functionality is the same as manually generating a scan report using the scan report generation button 
        in the UI for each individual scan.  

        When generating a scan report, an option UI appears allowing the selection of items to include in 
        the report.  Some of these items can be saved as a template so that they do not need to be selected for every
        report.  There are several options, however, that can not be persisted as a template and must be selected each time.

        The file support/soap/CxReportTemplate.psd1 can be edited to create a template that is used to generate each report.

    .PARAMETER sast_url
        The URL to the CxSAST instance.

    .PARAMETER username
        The name of the user in the CxSAST system.

    .PARAMETER password
        The password for the user in the CxSAST system.

    .PARAMETER dbg
        (Optional Flag) Runs in debug mode and prints verbose information to the screen while processing. 

    .PARAMETER report_type
        (Optional) Specifies the report type (CSV, PDF, RTF or XML). If not specified, PDF reports are generated.

    .PARAMETER report_teams
        (Optional) Only generate reports for projects belonging to the specified teams
#>
param(
    [Parameter(Mandatory = $true)]
    [System.Uri]$sast_url,
    [Parameter(Mandatory = $true)]
    [String]$username,
    [Parameter(Mandatory = $true)]
    [String]$password,
    [Switch]$dbg,
    [Parameter(Mandatory = $false)]
    [string]$report_type = "PDF",
    [Parameter(Mandatory = $false)]
    [string[]]$report_teams = @()
)

. "$PSScriptRoot/support/debug.ps1"

setupDebug($dbg.IsPresent)

$valid_report_types = @("CSV", "PDF", "RTF", "XML")
if (! $valid_report_types.Contains($report_type)) {
    Write-Error "$report_type is not a supported report type"
    Write-Error "Valid report types are $($valid_report_types -join `", `")"
    exit
}

$session = &"$PSScriptRoot/support/rest/sast/login.ps1" $sast_url $username $password -dbg:$dbg.IsPresent

$timer = $(Get-Date)
Write-Output "Fetching projects"
$projects = &"$PSScriptRoot/support/rest/sast/projects.ps1" $session
Write-Output "$($projects.Length) projects fetched - elapsed time $($(Get-Date).Subtract($timer))"
$projects | % { Write-Debug $_ } 

# refresh login, if needed
$session = &"$PSScriptRoot/support/rest/sast/login.ps1" -existing_session $session -dbg:$dbg.IsPresent


$timer = $(Get-Date)
Write-Output "Fetching teams"
$teams = &"$PSScriptRoot/support/rest/sast/teams.ps1" $session
Write-Output "$($teams.Length) teams fetched - elapsed time $($(Get-Date).Subtract($timer))"
$team_index = New-Object 'System.Collections.Generic.Dictionary[string,string]'
$team_name_index = New-Object 'System.Collections.Generic.Dictionary[string,string]'
$teams | % {
    $team_index.Add($_.id, $_.fullName)
    $team_name_index.Add($_.fullName, $_.id)
    Write-Debug $_ 
} 

$report_team_ids = New-Object 'System.Collections.Generic.List[int]'
$report_teams | % {
    if ( ! $_.StartsWith("/") ) {
        $_ = "/" + $_
    }
    if ( $team_name_index.ContainsKey($_) ) {
        $report_team_ids.Add($team_name_index[$_])
    } else {
        Write-Error "${_}: invalid team"
    }
}

Write-Debug "Report teams: $report_teams"
Write-Debug "Report team IDs: $report_team_ids"

Write-Output "Scans section starting"

$report_index = New-Object 'System.Collections.Generic.Dictionary[string,string]'
$scan_index = New-Object 'System.Collections.Generic.Dictionary[string,string]'
$prj_index = New-Object 'System.Collections.Generic.Dictionary[string,string]'

$projects | % {

    if ( $report_teams -and (! $report_team_ids.Contains($_.teamId)) ) {
        Write-Debug "Skipping project $($_.name) (in team $($_.teamId))"
    } else {

        $scans = &"$PSScriptRoot/support/rest/sast/scans.ps1" $session $_.id
        if ($scans) {
            $scan_index.Add($scans.id, $scans.owningTeamId)
            $prj_index.Add($scans.id, $scans.project.name)

            Write-Output $scans

            #generate the report
            $report = &"$PSScriptRoot/support/soap/generate_report.ps1" $session $scans.id $report_type
            $report_index.Add($scans.id, $report)
        } else {
            Write-Debug "No scans found for project $($_.id))"
        }
    }
}

#Probe for report completion
Write-Output "Checking status of all reports"
$report_index.Keys |%{
    $reportId = $report_index.Item($_)
    $reportstatus = &"$PSScriptRoot/support/rest/sast/reportStatus.ps1" $session $reportId
    
    while ($reportstatus.status.value -ne "Created" -and $reportstatus.status.value -ne "Failed") {
        Start-Sleep -Seconds 5
        $reportstatus = &"$PSScriptRoot/support/rest/sast/reportStatus.ps1" $session $reportId
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


    &"$PSScriptRoot/support/rest/sast/getreport.ps1" $session $reportid $teamName $projectName $outputPath $report_type.ToLower()

}
