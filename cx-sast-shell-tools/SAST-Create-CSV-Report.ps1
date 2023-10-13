<#

    .SYNOPSIS
        This script creates a CSV report of all the latest scans for the projects belonging to the the teams requested.  
        The format is the same as the CSV generated for a single scan with the addition of columns for "Team Path" and "Project Name".

    .DESCRIPTION
        The functionality is the same as manually generating a CSV scan report using the scan report generation button 
        in the UI for each individual scan, but the data is combined to create a single CSV with additional columns for team and project.

    .PARAMETER sast_url
        The URL to the CxSAST instance. For example, https://sast.xyz.com

    .PARAMETER overwrite_existing_report
        (Optional Flag) if present it will overwrite the existing report (with the same name - today's date stamp) if one exists.
        If the flag is not provided and a file exists, a prompt will appear to ask to overwrite (Y) or append (N).

    .PARAMETER dbg
        (Optional Flag) Runs in debug mode and prints verbose information to the screen while processing. 

    .FILE INPUT .\ReportTeams.txt
        (Mandatory file) The teams to be included in the report.

    .CREDENTIALS 
        Store credentials as "Windows Credentials" in Credential Manger under the key "CxSASTAPI" for the account used to run this script.
        It is requried to install the CredentialMangager module using the command:
            Install-Module -Name "CredentialManager"

#>
param(
    [Parameter(Mandatory = $true)]
    [System.Uri]$sast_url,
    [Switch]$overwrite_existing_report,
    [Switch]$dbg
)

#Set-ExecutionPolicy Bypass -scope Process -Force
cd $PSScriptRoot

. "$PSScriptRoot/support/debug.ps1"

setupDebug($dbg.IsPresent)

######## Checkmarx Config #########################################################
Write-Host "Getting stored credentials"
$credentialsSource = Get-StoredCredential -Target "CxSASTAPI" -AsCredentialObject
 
$username = $credentialsSource.UserName
$password = $credentialsSource.Password

Write-Debug "username ${username}"
###################################################################################

$report_type = "CSV"

if (Test-Path .\ReportTeams.txt) {
    $report_teams = Get-Content -Path .\ReportTeams.txt
    Write-Output "Creating report for the following teams: ${report_teams}"
} 
else {
    Write-Output "ReportTeams.txt not found - create the file with a team path on each line for the teams to be included in the report"
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
$date = Get-Date -Format "ddMMyyyy"
$outputPath = $PSScriptRoot + "\Output"
$reportOutputPath = [String]::Format("{0}\CxSAST_Scan_Data_{1}.{2}", $outputPath, $date, $report_type.ToLower() )
if (Test-Path $reportOutputPath) {
    if($overwrite_existing_report)
    {
        Remove-Item $reportOutputPath -verbose -Force
    }
    else {
        Remove-Item $reportOutputPath -verbose -Force -Confirm
    }
}

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

#$report_team_ids = New-Object 'System.Collections.Generic.List[int]'
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

            $directory = [String]::Format("{0}\{1}", $outputPath, $teamName )
            $filepath = [String]::Format("{0}\{1}_{2}.{3}", $directory, $projectName, $date, $report_type.ToLower() )
            $data = Import-CSV $filepath
            $directory = $outputPath
            $data | Select-Object *, @{n=”Team Path”;e={$teamName}}, @{n=”Project Name”;e={$projectName}} | Export-CSV $reportOutputPath -Append -NoTypeInformation
        }
    } else {
        Write-Error "${_}: invalid team"
    }
}

#Clean up - remove the team folders and individual report files
$teamRootFolder = $outputPath + "/CxServer"
if (Test-Path $teamRootFolder) {
    Remove-Item $teamRootFolder -Recurse -verbose -Force
} 