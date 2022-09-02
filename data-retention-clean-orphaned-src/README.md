# Orphaned CxSrc Folder Cleanup

When data retention purges scans, the source in CxSrc should also be purged.  In some cases, folders in CxSrc are orphaned by failures during data retention.  This leaves source code that consumes disk space in folders under CxSrc.  

This utility, when run on the CxManager, will purge the orphaned source folders under CxSrc.

## Operation

If the script is executed with the `-delete` option, no size calculation is performed.  The script begins the purge process immediately.

If executed **without** the `-delete` option, a size calculation is performed to find the amount of space that could be recovered.  No files will be deleted.

## Comand Line Parameters

`-delete` (*optional*): Deletes the files that are not associated with a scan record in CxDB.

`-cxsrc` (**required**): The directory path to `CxSrc` where scanned source code is stored.

`-sqlServer` (**required**): The name and optional instance for the SQL server hosting the CxDB database.

`-sqlUserName` (*optional*): If using SQL user authentication, the username for the SQL user.

`-sqlPassword` (*optional*): The password for the SQL user name provided with the `-sqlUserName` parameter.

`-threads` (*optional*): The maximum number of concurrent threads to use when performing operations.  If not set, the .Net default number of threads are used.

## Other Information

Detailed documentation can be obtained from the CxDR.ps1 script.  Place it on your CxManager and issue the following command in PowerShell to see detailed documentation:

`Get-Help CxDR.ps1 -full`


When executing the script, your execution policy may prevent `CxDR.ps1` from executing.  If so, the execution policy can be temporarily bypassed by executing `CxDR.ps1` via the following command in a PowerShell window running as administrator:

`PowerShell.exe -ExecutionPolicy Bypass -File CxDR.ps1 ... <args>`
