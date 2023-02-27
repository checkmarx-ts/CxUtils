NAME

    C:\path\CheckExclusionsFoldersFiles_local.ps1
    
SYNOPSIS

    Powershell script to Find Potential Folder/Files exclusions over a localy available CxSRC
    
    
SYNTAX

    C:\path\CheckExclusionsFoldersFiles_local.ps1 [-basedir] <String> 
    
    
DESCRIPTION

    For purposes of Project configuration tuning at large scale for all projects scanned, 
    it was created this Powershell script that goes over the CxSrc folder and find potential 
    Folders/Files exclusions in order to:
    - Reduce LOC
    - Reduce Time Scanning
    - Reduce FPs rate
    
PARAMETERS

    -basedir <String>
        Local src folder path
    
REMARKS

    For more information, checkout https://checkmarx.atlassian.net/wiki/spaces/AA/pages/6825215196/Quick+Exclusions
    Do not apply this exclusions blindly! Some customers alter 3rd party files introducing vulnerabilities.