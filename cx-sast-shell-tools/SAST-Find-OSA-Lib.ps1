<#

    .SYNOPSIS
        This script iterates projects in a Checkmarx SAST system and attempts to find libraries in OSA scans matching a pattern.

    .DESCRIPTION
        For users that have OSA, this will search libraries in any projects that have OSA scans.  Any library matching
        the supplied regular expression pattern will be displayed.

    .PARAMETER sast_url
        The URL to the CxSAST instance.

    .PARAMETER username
        The name of the user in the CxSAST system.

    .PARAMETER password
        The password for the user in the CxSAST system.

    .PARAMETER libraryPattern
        Defaults to ".*log4j.*".  The pattern that will be used to match the name of the library.

    .PARAMETER dbg
        (Optional Flag) Runs in debug mode and prints verbose information to the screen while processing. 

#>
param(
    [Parameter(Mandatory = $true)]
    [System.Uri]$sast_url,
    [Parameter(Mandatory = $true)]
    [String]$username,
    [Parameter(Mandatory = $true)]
    [String]$password,
    [String]$libraryPattern = ".*log4j.*",
    [Switch]$dbg
)

Add-Type -AssemblyName System.Runtime

. "$PSScriptRoot/support/debug.ps1"

setupDebug($dbg.IsPresent)


Write-Host "Searching OSA scans at [$sast_url] for libraries with names matching the pattern [$libraryPattern]"
$session = &"$PSScriptRoot/support/rest/sast/login.ps1" $sast_url $username $password -dbg:$dbg.IsPresent

$teams = @{}

$(&"$PSScriptRoot/support/rest/sast/teams.ps1" $session) | ForEach-Object {$teams[$_.id] = $_.fullName}
$projectsResponse = &"$PSScriptRoot/support/rest/sast/projects.ps1" $session


foreach ($project in $projectsResponse) {
    $lastOsaScan = &"$PSScriptRoot/support/rest/osa/scans.ps1" $session $project.id 1
    if ($null -ne $lastOsaScan) {
        $libs = $(&"$PSScriptRoot/support/rest/osa/libraries.ps1" $session $lastOsaScan.id)
        if ($libs.count -gt 0) {
            $re_matches =  [System.Collections.ArrayList]@()
            foreach($lib in $libs) {

                if ($true -eq [System.Text.RegularExpressions.Regex]::IsMatch($lib, $libraryPattern) ) {
                    $re_matches.Add($lib) | Out-Null
                }
            }
            if ($re_matches.count -gt 0) {
                Write-Host "Project: $($teams[$project.teamId])/$($project.name) OSA ScanId:" $lastOsaScan.id
                Write-Host "*** MATCHES FOUND ***"
                $re_matches | ForEach-Object {Write-Host $_}
            }
            else {
                Write-Host "Project: $($teams[$project.teamId])/$($project.name): NO MATCHES"
            }
        }
    }
}

Write-Host "SCAN FINISHED"