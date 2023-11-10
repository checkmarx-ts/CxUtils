# Shell Tools for CxSAST

This is a collection of PowerShell scripts that perform business functions by retrieving data from the CxSAST APIs.  These can be run from any machine that can make a connection to the CxSAST server.

Help is embedded in each script and can be obtained by executing the command `Get-Help <script-name> -full`.

# Tool Framework

More tool scripts may be added to this framework by utilizing the scripts in the `support` folder.  Scripts can be found there that implement common API calls.

The script `support/rest/sast/login.ps1`, for example, can be used to establish a session with CxSAST v8.9 or later.  The session can be used for executing other API scripts.

Most of the extension capability is intended to be available for Checkmarx employees to add tools to this framework.  As such, there is not comprehensive documentation for this toolkit as of the date of this document's publication.


# Available Shell Tools


| Name | Description |
|---|---|
| SAST-Create-Report | This script iterates projects in the SAST system and generates PDF reports for each scan using a user-defined template. |
| SAST-Dump-All-Queries | Dumps all CxQL queries currently in the system. |
| SAST-Find-OSA-Lib | Searches all OSA scans for libraries with a name matching a supplied pattern |
| SAST-Migrate-Project | Used to migrate project configurations from one instance of CxSAST to a new instance of CxSAST. |
| SAST-Purge-Branch-Projects.ps1 | Scans for branch projects, then optionally deletes them. |
| SAST-Purge-Empty-Projects.ps1 | Scans for projects containing 0 scans, then optionally deletes them. |
| SAST-Update-Result_State | Changes result state for multiple results when given an input CSV file. |
