# SAST Update Git Credentials

To see full documentation, execute the following command in PowerShell

```powershell
Get-Help -Full .\UpdateGitCredentials.ps1
Get-Help -Full .\HostToPATMap.ps1
```

This script will update Git credentials in SAST projects that have Git repository settings.  If no projects are specified, it attempt to update all projects.  Specific projects can be specified by Project ID or by full project name path (e.g. /CxServer/Team/ProjectName).

The help output provided execution examples.  By default, the script does not update the Git settings unless the `-write` option is provided as a command parameter.  This allows for review of the proposed changes before they are set on the projects.
