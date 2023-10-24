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

    .PARAMETER dbg
        (Optional Flag) Runs in debug mode and prints verbose information to the screen while processing. 

    .PARAMETER report_type
        (Optional) Specifies the report type (CSV, PDF, RTF or XML). If not specified, PDF reports are generated.

    .FILE INPUT .\ReportTeams.txt
        (Optional file) The teams to be included in the report.  If empty or no file is supplied then all teams will be used as default.

    .CREDENTIALS 
        Store credentials as "Windows Credentials" in Credential Manger under the key "CxSASTAPI" for the account used to run this script.
        It is requried to install the CredentialMangager module using the command:
            Install-Module -Name "CredentialManager"
#>
param(
    [Parameter(Mandatory = $true)]
    [System.Uri]$sast_url,
    [Switch]$dbg,
    [Parameter(Mandatory = $false)]
    [string]$report_type = "PDF"
)

. "$PSScriptRoot/support/debug.ps1"

setupDebug($dbg.IsPresent)

$valid_report_types = @("CSV", "PDF", "RTF", "XML")
if (! $valid_report_types.Contains($report_type)) {
    Write-Error "$report_type is not a supported report type"
    Write-Error "Valid report types are $($valid_report_types -join `", `")"
    exit
}

######## Checkmarx Config #########################################################
Write-Host "Getting stored credentials"
$credentialsSource = Get-StoredCredential -Target "CxSASTAPI" -AsCredentialObject
 
$username = $credentialsSource.UserName
$password = $credentialsSource.Password

Write-Debug "username ${username}"
###################################################################################

$session = &"$PSScriptRoot/support/rest/sast/login.ps1" $sast_url $username $password -dbg:$dbg.IsPresent

if (Test-Path .\ReportTeams.txt) {
    $report_teams = Get-Content -Path .\ReportTeams.txt
    Write-Output "Creating ${report_type} reports for the latest scan for projects in the following teams: ${report_teams}"
} 
else {
    Write-Output "ReportTeams.txt not found - will produce ${report_type} report for the latest scan for projects in all teams"
}

$timer = $(Get-Date)
Write-Output "Fetching projects"
$projects = &"$PSScriptRoot/support/rest/sast/projects.ps1" $session
Write-Output "$($projects.Length) projects fetched - elapsed time $($(Get-Date).Subtract($timer))"
$projects | % { Write-Debug $_ } 

# refresh login, if needed
$session = &"$PSScriptRoot/support/rest/sast/login.ps1" -existing_session $session -dbg:$dbg.IsPresent

$timer = $(Get-Date)
$outputPath = $PSScriptRoot + "\Output"

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

if($report_teams -eq $null) {
    $report_teams = $team_name_index.Keys
}


$report_teams | % {
    if ( ! $_.StartsWith("/") ) {
        $_ = "/" + $_
    }
    if ( $team_name_index.ContainsKey($_) ) {
        $report_team_id = $team_name_index[$_]

        Write-Debug "Report team: $_"
        Write-Debug "Report team ID: $report_team_id"

        Write-Output "Scans section starting"

        
        $scan_ids = New-Object 'System.Collections.Generic.List[int]'
        $scan_index = New-Object 'System.Collections.Generic.Dictionary[string,string]'
        $prj_index = New-Object 'System.Collections.Generic.Dictionary[string,string]'

        $projects | % {

            if ( $report_teams -and ($report_team_id -ne ($_.teamId)) ) {
                Write-Debug "Skipping project $($_.name) (in team $($_.teamId))"
            } else {

                $scans = &"$PSScriptRoot/support/rest/sast/scans.ps1" $session $_.id
                if ($scans) {
                    $scan_index.Add($scans.id, $scans.owningTeamId)
                    $prj_index.Add($scans.id, $scans.project.name)
                    $scan_ids.Add($scans.id)
                    Write-Output $scans

                } else {
                    Write-Debug "No scans found for project $($_.id))"
                }
            }
        }

        $report_index = New-Object 'System.Collections.Generic.Dictionary[string,string]'
        $scanIterationCounter = 0
        $totalScans = $scan_index.Count
        $scan_ids | % {
            #generate the report
            $scanid = $_
            $reportId = &"$PSScriptRoot/support/soap/generate_report.ps1" $session $scanid $report_type
            $report_index.Add($scanid, $reportId)
            $reportCounter = $reportCounter + 1
        
            Write-Output "Requested scan report for scan id ${scanid}"  

            #Probe for report completion
            Write-Output "Checking status of report id ${reportId}"
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
            #}

            Write-Output "Report created ${reportId}"

            #Download the requested report
            Write-Output "Downloading report ${reportId}"
            
            $teamid = $scan_index.Item($_)
            $teamName = $team_index.Item($teamid)
            $projectName = $prj_index.Item($_)

            Write-Debug "ScanId = $scanid , team name = $teamName, project name = $projectName, reportId = $reportid"
            Write-Output "Downloading report for $teamName\$projectName"


            &"$PSScriptRoot/support/rest/sast/getreport.ps1" $session $reportid $teamName $projectName $outputPath $report_type.ToLower()
        }
    } else {
        Write-Error "${_}: invalid team"
    }
}