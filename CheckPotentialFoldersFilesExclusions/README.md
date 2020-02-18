NAME

    C:\path\CheckExclusionsFoldersFiles.ps1
    
SYNOPSIS

    Powershell script to Find Potential Folder/Files exclusions over CxSRC
    
    
SYNTAX

    C:\path\CheckExclusionsFoldersFiles.ps1 [-cxserver] <String> [-cxUsername] 
    <String> [-cxPassword] <String> [-cxSrcFolder] <String> [-generatedFile] <String> [<CommonParameters>]
    
    
DESCRIPTION

    For purposes of Project configuration tuning at large scale for all projects scanned, 
    it was created this Powershell script that goes over the CxSrc folder and find potential 
    Folders/Files exclusions in order to:
    - Reduce LOC
    - Reduce Time Scanning
    - Reduce FPs rate
    
PARAMETERS

    -cxserver <String>
        Checkmarx Server URL (i.e. https://checkmarx.company.com)
        
    -cxUsername <String>
        Checkmarx Username (i.e. first.last@company.com)
        
    -cxPassword <String>
        Checkmarx Password
        
    -cxSrcFolder <String>
        Checkmarx Source Folder (i.e. D:\CxSrc)
        
    -generatedFile <String>
        Exclusions file generated (i.e. D:\exclusions.json)
        
    <CommonParameters>
        This cmdlet supports the common parameters: Verbose, Debug,
        ErrorAction, ErrorVariable, WarningAction, WarningVariable,
        OutBuffer, PipelineVariable, and OutVariable. For more information, see 
        about_CommonParameters (https:/go.microsoft.com/fwlink/?LinkID=113216). 
    
REMARKS

    To see the examples, type: "get-help C:\path\CheckExclusionsFoldersFiles.ps1 -examples".

    For more information, type: "get-help C:\path\CheckExclusionsFoldersFiles.ps1 -detailed".
    
    For technical information, type: "get-help C:\path\CheckExclusionsFoldersFiles.ps1 -full".