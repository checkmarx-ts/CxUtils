<#
.SYNOPSIS
    Version 1.2
.DESCRIPTION
    This script can be used to find scan directories that should have been removed 
    by CxSAST data retention functionality.  It is meant to supplement data retention 
    capabilities until bug 175055 is resolved by R&D.  Without the -delete switch, this 
    script will only determine the amount of disk space that will be released if the 
    scans were deleted from CxSRC.
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
.PARAMETER threads
    The maximum number of concurrent threads.  If not supplied, the .Net default is used.
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

    Update: Nathan Leach
    Date:   September 2, 2022
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
    [string]$sqlPassword,

    [Parameter(Mandatory=$false)]
    [string]$threads=0
 )

#variable declarations
$query = "SELECT CONCAT('$cxsrc',ProjectId,'_',SourceId) AS FullPath FROM CxEntities.Scan"
$scansInCxSRC = 0
$scansToKeep = 0

Write-Host "Reading directory $cxsrc"
#Get all directories in CxSRC
$scansInCxSRC = (Get-ChildItem $cxsrc).FullName
Write-Host "Finished reading directory, $($scansInCxSRC.Count) folders found."

#Get all scans in the scan view of CxDB -- these should be the same scans as what's in CxSRC
Write-Host "Reading scans from database"

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

Write-Host "Finished reading scans from database"

# {scans in CxSRC} - {scans in CxDB} --> {scans that should be deleted from CxSRC}
$scansToDelete = $scansInCxSRC | Where {$scansToKeep -NotContains $_}


$threading = @"
using System;
using System.IO;
using System.Threading;
using System.Threading.Tasks;
using System.Collections.Concurrent;
using System.Runtime.CompilerServices;



public class OrphanSourcePurge
{
    private ConcurrentBag<String> _targetDirs = new ConcurrentBag<string>();

    private static readonly Double SIZE_DIVISOR = 1024000.0;

    private ParallelOptions _opts;

    class Reporter : IDisposable
    {
        private long _maxSize;
        private long _progress;
        private int _previousStrLen = 0;
        private String _label;
        private int _interval;
        DateTime _start = DateTime.Now;

        public Reporter(String label, long maxSize, int interval = 3)
        {
            _maxSize = maxSize;
            _label = label;
            _interval = interval;
        }

        public void Dispose()
        {
            var elapsed = DateTime.Now.Subtract(_start);

            Console.WriteLine(String.Format(" ({0:F2}ms)", elapsed.TotalMilliseconds) );
        }

        [MethodImpl(MethodImplOptions.Synchronized)]
        public void UpdateProgress(long by = 1)
        {
            _progress += by;
            
            int percent = (int)((_progress / (double)_maxSize) * 100.0);

            if (percent % _interval == 0 || _progress >= _maxSize)
            {
                Console.Write("".PadLeft(_previousStrLen, '\b'));
                String display = String.Format("{0} {1}%", _label, percent);
                _previousStrLen = display.Length;
                Console.Write(display);
            }
        }
    }


    public OrphanSourcePurge(Object[] deleteDirectories, int concurrentThreads = 0)
    {
        _opts = new ParallelOptions();

        if (concurrentThreads > 0)
            _opts.MaxDegreeOfParallelism = concurrentThreads;


        Parallel.ForEach(deleteDirectories, _opts, (dir) => {

            if (dir != null)
                _targetDirs.Add(dir.ToString());
        });
    }

    public double GetSizeInMB()
    {
        long size = 0;

        using (var progress = new Reporter("Calculating size: ", _targetDirs.Count))
            Parallel.ForEach(_targetDirs, _opts, (dir) =>
            {
                var files = Directory.EnumerateFiles(dir, "*", SearchOption.AllDirectories);
                Parallel.ForEach(files, _opts, (f) =>
                {
                    var fi = new FileInfo(f);
                    Interlocked.Add(ref size, new FileInfo(f).Length);
                });
                progress.UpdateProgress();
            });

        return size / SIZE_DIVISOR;
    }


    public void Delete()
    {
        using (var progress = new Reporter("Deleting directories: ", _targetDirs.Count))
            Parallel.ForEach(_targetDirs, _opts, (dir) =>
            {
                Directory.Delete(dir, true);
                progress.UpdateProgress();
            });
    }
}
"@

if (-not ("OrphanSourcePurge" -as [type]))
{
    Add-Type -TypeDefinition $threading -Language CSharp
}

$purgeObj = [OrphanSourcePurge]::new($scansToDelete, $threads)

if ($delete -eq $False)
{
    $mbSize = $purgeObj.GetSizeInMB();

    Write-Host $("{0:N2} MB to delete" -f $mbSize)
}
else 
{
    $purgeObj.Delete()
}

