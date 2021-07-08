<#
.SYNOPSIS
    Version 1.2
.DESCRIPTION
    This script can be used to find scan directories that should have been removed 
    by CxSAST data retention functionality.  It is meant to supplement data retention 
    capabilities until bug 175055 is resolved by R&D.  Without the -delete switch, this 
    script will only identify folders that should have been removed by data retention and 
    determine the amount of disk space that will be released if the scans were deleted 
    from CxSRC.
.PARAMETER delete
    Removes files from the file system that should have been removed by CxSAST data retention
.PARAMETER cxsrc
    Full path to CxSRC, must include trailing '\'
.PARAMETER sqlServer
    Name of SQL server used by CxSAST
.PARAMETER sqlUserName
    SQL server user if using SQL auth
.PARAMETER sqlPassword
    Password for SQL server user if using SQL auth
.EXAMPLE
    .\CxDR.ps1 -cxsrc C:\CxSrc\ -sqlServer WIN-04MAT5MP9H1\SQLEXPRESS
    This will only analyze CxSRC; it will not delete anything.  It will also use integrated auth to authenticate to the SQL server.
.EXAMPLE
    .\CxDR.ps1 -cxsrc C:\CxSrc\ -sqlServer WIN-04MAT5MP9H1\SQLEXPRESS -sqlUserName sa -sqlPassword mypassword
    Use the optional flags -sqlUserName and -sqlPassword to authenticate to the SQL server using SQL Auth.
.EXAMPLE
    .\CxDR.ps1 -cxsrc C:\CxSrc\ -sqlServer WIN-04MAT5MP9H1\SQLEXPRESS -delete
    This will delete folders from the file system that should have been deleted by CxSAST data retention; it will use integrated auth to authenticate to the SQL server.
.NOTES
    Author: Chris Merritt
    Date:   August 31, 2019    
#>

 param (
    [Parameter(Mandatory=$false)]
    [switch]$delete, 

    [Parameter(Mandatory=$true)]
    [string]$cxsrc,

    [Parameter(Mandatory=$true)]
    [string]$sqlServer,

    [Parameter(Mandatory=$false)]
    [string]$sqlUserName,

    [Parameter(Mandatory=$false)]
    [string]$sqlPassword
 )

#variable declarations
$query = "SELECT CONCAT('$cxsrc',ProjectId,'_',SourceId) AS FullPath FROM CxEntities.Scan"
$totalSize = 0
$printMe = @()
$i = 0
$deletedCount = 0
$deletedSize = 0

#Get all directories in CxSRC
$scansInCxSRC = (Get-ChildItem $cxsrc).FullName

#Get all scans in the scan view of CxDB -- these should be the same scans as what's in CxSRC
try {
    if(!$sqlUserName -and !$sqlPassword) {
        $scansToKeep = (Invoke-Sqlcmd -Query $query -ServerInstance $sqlServer -Database "CxDB" -ErrorAction Stop).FullPath
    } else {
        $scansToKeep = (Invoke-Sqlcmd -Query $query -ServerInstance $sqlServer -Database "CxDB" -Username $sqlUserName -Password $sqlPassword -ErrorAction Stop).FullPath
    }
} catch {
    Write-Host $Error[0] -ForegroundColor Red
    exit
}

# {scans in CxSRC} - {scans in CxDB} --> {scans that should be deleted from CxSRC}
$scansToDelete = $scansInCxSRC | Where {$scansToKeep -NotContains $_}

foreach($scan in $scansToDelete){
    
    #get the size of the directory that should have been deleted
    try {
        $size = ((Get-ChildItem $scan -Recurse | Measure-Object -Property Length -Sum).Sum / 1MB)
        $totalSize += $size
        $printMe += [pscustomobject]@{Directory = $scan; Size = "{0:N2} MB" -f $size}
    } catch {
        $printMe += [pscustomobject]@{Directory = $scan; Size = "ERROR"}
    }

    #if the delete switch is set, delete the directory that should have been deleted by data retention
    if($delete -eq $true){
        try {
            Write-Host "Deleting $($scan) ($("{0:N2} MB" -f $size))."
            Remove-Item -LiteralPath $scan -Force -Recurse -ErrorAction Stop
            $deletedCount++
            $deletedSize += $size
        } catch {
            Write-Host "Could not delete $($scan)." -ForegroundColor Red
        }
    }

    #just tracking progress here...
    $i++
    $percomplete = $i / $scansToDelete.Count * 100
    Write-Progress -Activity "Calculating directory sizes" -Status "$percomplete% Complete:" -PercentComplete $percomplete;
}

#Print a summary of what should be deleted if the delete switch is not set OR print the total number of scans + freed storage space
if($delete -eq $false) {
    $printMe | Format-Table
    Write-Host "$($scansToDelete.Count) scan(s) ($("{0:N2} GB" -f ($totalSize/1000))) should be deleted."
} else {
    Write-Host "`n$($deletedCount) scan(s) ($("{0:N2} GB" -f ($deletedSize/1000))) deleted."
}