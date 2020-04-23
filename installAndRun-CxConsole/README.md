### installAndRun-CxConsole

A powershell script to auto-download and execute the CxConsolePlugin (Checkmarx CLI)

The script is a wrapper to the CxConsolePlugin. 
    https://checkmarx.atlassian.net/wiki/spaces/KC/pages/914096139/CxSAST+CxOSA+Scan+v8.9.0

### Usage

.\CxScan.ps1  [-sastVersion &lt;sast_version&gt;] [-cliPlugin &lt;plugin_filename&gt;] -op [Scan | AsyncScan | OsaScan | AsyncOsaScan | GenerateToken |  RevokeToken] *{Other_CxConsolePlugin Params}*

### Default Values

If the optional -sastVersion and -cliPlugin values are not provided, the script defaults to the following:

*sastVersion* = 8.9
*cliPlugin* = CxConsolePlugin-8.90.2

The script downloads the CxConsolePlugin from:
https://download.checkmarx.com/$sastVersion/Plugins/$cliPluginFile

### Sample usage

#### SAST scan
.\CxScan.ps1  **-op Scan** -v -ProjectName "CxServer\Americas\Engineering\Development\DVJA" -CxServer https://my_checkmarx_host -cxuser admin -cxpassword myPassword -locationtype folder -locationpath "C:\shared\workspace\dvja" -preset "Checkmarx Default"

#### SAST + OSA
.\CxScan.ps1  **-op Scan** -v -Projectname "CxServer\Americas\Engineering\Development\DVJA" -CxServer https://my_checkmarx_host -cxuser admin -cxpassword myPassword -locationtype folder -locationpath "C:\shared\workspace\dvja" -preset "Checkmarx Default" **–EnableOsa** -executepackagedependency -OsaJson

#### OSA
.\CxScan.ps1  **-op OsaScan** -v -Projectname "CxServer\Americas\Engineering\Development\DVJA" -CxServer https://my_checkmarx_host -cxuser admin -cxpassword myPassword -locationtype folder -locationpath "C:\shared\workspace\dvja" -OsaFilesExclude .jpg,.jpeg -OsaPathExclude test -EnableOsa -executepackagedependency -Log .\osa_scan.log

#### SAST scan with specific CxSAST Versions
.\CxScan.ps1  **-sastVersion "8.9.0" -cliPlugin "CxConsolePlugin-8.90.2" -op Scan** -v -ProjectName "CxServer\Americas\Engineering\Development\DVJA" -CxServer https://my_checkmarx_host -cxuser admin -cxpassword myPassword -locationtype folder -locationpath "C:\shared\workspace\dvja" -preset "Checkmarx Default"

.\CxScan.ps1  **-sastVersion "8.8.0" -cliPlugin "CxConsolePlugin-8.80.2" -op Scan** -v -ProjectName "CxServer\Americas\Engineering\Development\DVJA" -CxServer https://my_checkmarx_host -cxuser admin -cxpassword myPassword -locationtype folder -locationpath "C:\shared\workspace\dvja" -preset "Checkmarx Default"

