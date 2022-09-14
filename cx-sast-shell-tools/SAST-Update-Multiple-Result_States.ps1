<#

    .SYNOPSIS
        Changes result state for multiple results when given an scan id.

    .DESCRIPTION
        This script is experimental.

    .PARAMETER SastUrl
        The URL to the CxSAST instance.

    .PARAMETER Username
        The name of the user in the CxSAST system.

    .PARAMETER Password
        The password for the user in the CxSAST system.

    .PARAMETER ScanId
        The scan id with the results you want to update.

    .PARAMETER ResultSeverity
        The result severity you want to filter by.

    .PARAMETER CurrentResultState
        The result state you want to filter by.

    .PARAMETER NewResultState
        The result state you want to update to.

    .PARAMETER dbg
        (Optional Flag) Runs in debug mode and prints verbose information to the screen while processing. 

#>
param(
    [Parameter(Mandatory = $true)]
    [System.Uri]$SastUrl,
    [Parameter(Mandatory = $true)]
    [String]$Username,
    [Parameter(Mandatory = $true)]
    [String]$Password,
    [Parameter(Mandatory = $true)]
    [int]$ScanId,
    [Parameter(Mandatory = $true)]
    [ValidateSet("Information", "Low", "Medium", "High")]
    [String]$ResultSeverity = "High",
    [Parameter(Mandatory = $true)]
    [ValidateSet("To Verify", "Not Exploitable", "Confirmed", "Urgent", "Proposed Not Exploitable")]
    [String]$CurrentResultState = "To Verify",
    [Parameter(Mandatory = $true)]
    [ValidateSet("To Verify", "Not Exploitable", "Confirmed", "Urgent", "Proposed Not Exploitable")]
    [String]$NewResultState = "Confirmed",
    [Switch]$dbg
)

. "$PSScriptRoot/support/debug.ps1"

setupDebug($dbg.IsPresent)

<# Get token for web service authorization #>
$Session = &"$PSScriptRoot/support/rest/sast/login.ps1" $SastUrl $Username $Password -dbg:$dbg.IsPresent

<# Get Results From OData endpoint #>
if($ResultSeverity && $CurrentResultState) {
    $Output = &"$PSScriptRoot/support/odata/GetScanResultsById.ps1" $Session $ScanId $ResultSeverity $CurrentResultState
}

Write-Host $Output.Value.Count
Write-Host $Output.Value.pathId

$PathIds = $Output.Value

<# Update Results #>

$Continue = Read-Host "Would you like to continue?"

if($Continue -eq "N") {
    exit
}

$UpdateComment = "Automatic result state change"

$ResultStateIds = @{
    "To Verify" = "0";
    "Not Exploitable" = "1";
    "Confirmed" = "2";
    "Urgent" = "3";
    "ProposedNotExploitable" = "4";
}

$ResultStateId = $ResultStateIds[$NewResultState]

$PathIds | ForEach-Object {
    &"$PSScriptRoot/support/rest/sast/patchResult.ps1" $Session $ScanId $_.PathId $ResultStateId $UpdateComment
    
    $Output = [String]::Format("Result state of scan: {0} pathId: {1} has been updated to {2}", $ScanId, $_.pathId, $NewResultState)
    Write-Output $Output
}

Write-Output "All records have been successfully updated"
