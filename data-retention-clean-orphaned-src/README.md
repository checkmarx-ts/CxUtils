# Orphaned CxSrc Folder Cleanup

When data retention purges scans, the source in CxSrc should also be purged.  In some cases, folders in CxSrc are orphaned by failures during data retention.  This leaves source code that consumes disk space in folders under CxSrc.  

This utility, when run on the CxManager, will purge the orphaned source folders under CxSrc.

## Usage

The usage is documented in the CxDR.ps1 script.  Place it on your CxManager and issue the following command in PowerShell to see how to use the script:

`Get-Help CxDR.ps1 -full`


When executing the script, your execution policy may prevent `CxDR.ps1` from executing.  If so, the execution policy can be temporarily bypassed by executing `CxDR.ps1` via the following command in a PowerShell window running as administrator:

`PowerShell.exe -ExecutionPolicy Bypass -File CxDR.ps1 ... <args>`
