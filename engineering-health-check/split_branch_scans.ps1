<#
.SYNOPSIS
Split out branch scans from EHC scan data
.DESCRIPTION
When a project is branched in CxSAST, a copy is made of the last scan
of the project that it was branched from. This script takes a JSON
file of scan data, extracted by the cxInsight script, and splits it
into two JSON files, one containing the actual scans that were
performed, and one containing the scans created on project branching.
.PARAMETER FileName
The name of the file containing the EHC scan data
.EXAMPLE
PS C:\> .\split_branch_scans.ps1 scan-data.json
.NOTES
Author : Checkmarx Professional Services
Date   : 2023-06-30
Updated: 2023-06-30
#>
param (
    [Parameter(Mandatory=$true)]
    [string]$FileName
)

$ScanData = Get-Content $FileName | ConvertFrom-Json
$ScanKeys = @{}
$BaseScanData = @{
    '@odata.context' = $ScanData."@odata.context"
    value = [System.Collections.ArrayList]::new()
}
$BranchScanData = @{
    # We intentionlly do not add the @odata.context property as, later, we
    # add a property (the original scan Id) and it doesn't seem worthwhile
    # going to the trouble of creating a fake context.
    value = [System.Collections.ArrayList]::new()
}

foreach ($scan in $ScanData.value) {
    $ScanKey = @($scan.OwningTeamId, $Scan.ProductVersion,
                 $scan.EngineServerId, $scan.Origin, $scan.PresetName,
                 $scan.RequestedOn, $scan.QueuedOn, $scan.EngineStartedOn,
                 $scan.EngineFinishedOn, $scan.ScanCompletedOn,
                 $scan.ScanDuration, $scan.FileCount, $scan.LOC,
                 $scan.FailedLOC, $scan.TotalVulnerabilities,
                 $scan.High, $scan.Medium, $scan.Low, $scan.Info,
                 $scan.IsIncremental, $scan.IsPublic) -join '-'
    if ($ScanKeys.ContainsKey($ScanKey)) {
        $OrigScanId = $ScanKeys[$ScanKey]
        $Scan | Add-Member -MemberType NoteProperty -Name OrigScanId -Value $OrigScanId
        $_ = $BranchScanData.value.Add($scan)
    } else {
        $_ = $BaseScanData.value.Add($scan)
        $ScanKeys[$ScanKey] = $scan.Id
    }
}

$bits = $FileName.split(".")
if ($bits.Count -gt 1) {
    $n = $bits.Count - 2
    $root = $bits[0..$n] -join "."
    $suff = $bits[$bits.Count - 1]
    $BaseScanFileName = $root + "-base." + $suff
    $BranchScanFileName = $root + "-branch." + $suff
} else {
    $BaseScanFileName = $FileName + "-base"
    $BranchScanFileName = $FileName + "-branch"
}

$BaseScanData | ConvertTo-Json -Depth 4 | Out-File $BaseScanFileName
$BranchScanData | ConvertTo-Json -Depth 4 | Out-File $BranchScanFileName
