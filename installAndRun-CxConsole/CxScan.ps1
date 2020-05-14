<#
    Checkmarx SAST and OSA Scan Initiator. Delegates to the CxConsolePlugin.
    Built for v8.9
    Checkmarx Professional Services

    Usage: .\CxScan.ps1 -op [Scan, AsyncScan, OsaScan, AsyncOsaScan, GenerateToken, RevokeToken] {CxConsolePlugin Params}
    
    This is a wrapper to the CxConsolePlugin. The parameters are documented here:
    https://checkmarx.atlassian.net/wiki/spaces/KC/pages/914096139/CxSAST+CxOSA+Scan+v8.9.0
#>
Param(

    [Parameter(Mandatory = $False)]
    [ValidateNotNullOrEmpty()]
    [String]
    $sastVersion = "8.9.0",
    
    [Parameter(Mandatory = $False)]
    [ValidateNotNullOrEmpty()]
    [String]
    $cliPlugin = "CxConsolePlugin-8.90.2",  

    [Parameter(Mandatory = $True)]
    [ValidateNotNullOrEmpty()]
    [String] $op,

    [Parameter(Mandatory = $True)]
    [ValidateNotNullOrEmpty()]
    [String] $CxServer,

    [switch]
    $useSSO,

    [Parameter(Mandatory = $False)]
    [ValidateNotNullOrEmpty()]
    [String] $CxUser,
    
    [Parameter(Mandatory = $False)]
    [ValidateNotNullOrEmpty()]
    [String] $CxPassword,

    [Parameter(Mandatory = $False)]
    [ValidateNotNullOrEmpty()]
    [String] $CxToken,
	
    [switch]
    $enableOsa,
    
    [Parameter(Mandatory = $False)]
    [ValidateNotNullOrEmpty()]
    [String] $OsaLocationPath,
    
    [Parameter(Mandatory = $False)]
    [ValidateNotNullOrEmpty()]
    [String] $ProjectName,
    
    [Parameter(Mandatory = $False)]
    [ValidateNotNullOrEmpty()]
    [String] $LocationType,
    
    [Parameter(Mandatory = $False)]
    [ValidateNotNullOrEmpty()]
    [String] $WorkspaceMode,

    [Parameter(Mandatory = $False)]
    [ValidateNotNullOrEmpty()]
    [String] $LocationPath,
    
    [Parameter(Mandatory = $False)]
    [ValidateNotNullOrEmpty()]
    [String] $LocationURL,
    
    [Parameter(Mandatory = $False)]
    [ValidateNotNullOrEmpty()]
    [String] $LocationPort,
    
    [Parameter(Mandatory = $False)]
    [ValidateNotNullOrEmpty()]
    [String] $LocationBranch,
    
    [Parameter(Mandatory = $False)]
    [ValidateNotNullOrEmpty()]
    [String] $LocationUser,
    
    [Parameter(Mandatory = $False)]
    [ValidateNotNullOrEmpty()]
    [String] $LocationPassword,
    
    [Parameter(Mandatory = $False)]
    [ValidateNotNullOrEmpty()]
    [String] $LocationPrivateKey,
    
    [Parameter(Mandatory = $False)]
    [ValidateNotNullOrEmpty()]
    [String] $LocationPublicKey,
    
    [Parameter(Mandatory = $False)]
    [ValidateNotNullOrEmpty()]
    [String] $Preset,
    
    [switch]
    $ForceScan,

    [switch]
    $Incremental,

    [Parameter(Mandatory = $False)]
    [ValidateNotNullOrEmpty()]
    [String] $LocationPathExclude,
    
    [Parameter(Mandatory = $False)]
    [ValidateNotNullOrEmpty()]
    [String] $LocationFilesExclude,
    
    [Parameter(Mandatory = $False)]
    [ValidateNotNullOrEmpty()]
    [String] $SASTHigh,
    
    [Parameter(Mandatory = $False)]
    [ValidateNotNullOrEmpty()]
    [String] $SASTMedium,
    
    [Parameter(Mandatory = $False)]
    [ValidateNotNullOrEmpty()]
    [String] $SASTLow,
    
    [Parameter(Mandatory = $False)]
    [ValidateNotNullOrEmpty()]
    [String] $Configuration,
    
    [switch]
    $Private,

    [Parameter(Mandatory = $False)]
    [ValidateNotNullOrEmpty()]
    [String] $Log,

    [Parameter(Mandatory = $False)]
    [ValidateNotNullOrEmpty()]
    [String] $OsaArchiveToExtract,
    
    [Parameter(Mandatory = $False)]
    [ValidateNotNullOrEmpty()]
    [String] $OsaFilesInclude,

    [Parameter(Mandatory = $False)]
    [ValidateNotNullOrEmpty()]
    [String] $OsaFilesExclude,
    
    [Parameter(Mandatory = $False)]
    [ValidateNotNullOrEmpty()]
    [String] $OsaPathExclude,
    
    [Parameter(Mandatory = $False)]
    [ValidateNotNullOrEmpty()]
    [String] $OsaScanDepth,
    
    [switch]
    $executepackagedependency,

    [Parameter(Mandatory = $False)]
    [ValidateNotNullOrEmpty()]
    [String] $OSAHigh,
    
    [Parameter(Mandatory = $False)]
    [ValidateNotNullOrEmpty()]
    [String] $OSAMedium,
    
    [Parameter(Mandatory = $False)]
    [ValidateNotNullOrEmpty()]
    [String] $OSALow,
    
    [Parameter(Mandatory = $False)]
    [ValidateNotNullOrEmpty()]
    [String] $OsaReportHtml,
    
    [Parameter(Mandatory = $False)]
    [ValidateNotNullOrEmpty()]
    [String] $OsaReportPDF,
    
    [Parameter(Mandatory = $False)]
    [ValidateNotNullOrEmpty()]
    [String] $OsaJson,
    
    [Parameter(Mandatory = $False)]
    [ValidateNotNullOrEmpty()]
    [String] $ReportXML,
    
    [Parameter(Mandatory = $False)]
    [ValidateNotNullOrEmpty()]
    [String] $ReportPDF,
    
    [Parameter(Mandatory = $False)]
    [ValidateNotNullOrEmpty()]
    [String] $ReportCSV,
    
    [Parameter(Mandatory = $False)]
    [ValidateNotNullOrEmpty()]
    [String] $ReportRTF,
    
    [Parameter(Mandatory = $False)]
    [ValidateNotNullOrEmpty()]
    [String] $Comment,
    
    [switch]
    $v,
    
    [Parameter(Mandatory = $False)]
    [ValidateNotNullOrEmpty()]
    [String] $CheckPolicy    
)

function createCommand () {

    # Basic command
    $cmd = "runCxConsole.cmd $op"

    # Verbose output requested?
    $cmd += if ($v) { " -v" } else { "" }

    # Server parameters
    $cmd += if ($CxServer) { " -CxServer $CxServer" } else { "" }

    # Authentication parameters    
    $cmd += if ($useSSO) { " -useSSO" } else { "" }
    $cmd += if ($CxToken) { " -CxToken $CxToken" } else { "" }
    $cmd += if ($CxUser) { " -CxUser $CxUser" } else { "" }
    $cmd += if ($CxPassword) { " -CxPassword `"$CxPassword`"" } else { "" }    

    # Project / source parameters
    $cmd += if ($ProjectName) { " -ProjectName `"$ProjectName`"" } else { "" }    
    $cmd += if ($LocationType) { " -LocationType $LocationType" } else { "" }
    $cmd += if ($LocationPath) { " -LocationPath `"$LocationPath`"" } else { "" }
    $cmd += if ($WorkspaceMode) { " -WorkspaceMode $WorkspaceMode" } else { "" }
    $cmd += if ($LocationURL) { " -LocationURL `"$LocationURL`"" } else { "" }
    $cmd += if ($LocationPort) { " -LocationPort $LocationPort" } else { "" }
    $cmd += if ($LocationBranch) { " -LocationBranch `"$LocationBranch`"" } else { "" }
    $cmd += if ($LocationUser) { " -LocationUser $LocationUser" } else { "" }
    $cmd += if ($LocationPassword) { " -LocationPassword `"$LocationPassword`"" } else { "" }
    $cmd += if ($LocationPrivateKey) { " -LocationPrivateKey `"$LocationPrivateKey`"" } else { "" }
    $cmd += if ($LocationPublicKey) { " -LocationPublicKey `"$LocationPublicKey`"" } else { "" }
    $cmd += if ($LocationPathExclude) { " -LocationPathExclude `"$LocationPathExclude`"" } else { "" }
    $cmd += if ($LocationFilesExclude) { " -LocationFilesExclude `"$LocationFilesExclude`"" } else { "" }

    # SAST Scan Parameters
    $cmd += if ($Preset) { " -Preset `"$Preset`"" } else { "" }
    $cmd += if ($Configuration) { " -Configuration `"$Configuration`"" } else { "" }
    $cmd += if ($ForceScan) { " -ForceScan" } else { "" }
    $cmd += if ($Incremental) { " -Incremental" } else { "" }
    $cmd += if ($Private) { " -Private" } else { "" }
    $cmd += if ($SASTHigh) { " -SASTHigh $SASTHigh" } else { "" }
    $cmd += if ($SASTMedium) { " -SASTMedium $SASTMedium" } else { "" }
    $cmd += if ($SASTLow) { " -SASTLow $SASTLow" } else { "" }
    $cmd += if ($ReportXML) { " -ReportXML `"$ReportXML`"" } else { "" }
    $cmd += if ($ReportPDF) { " -ReportPDF `"$ReportPDF`"" } else { "" }
    $cmd += if ($ReportCSV) { " -ReportCSV `"$ReportCSV`"" } else { "" }
    $cmd += if ($ReportRTF) { " -ReportRTF `"$ReportRTF`"" } else { "" }
    $cmd += if ($Comment) { " -Comment `"$Comment`"" } else { "" }
    
    # OSA Scan Parameters
    $cmd += if ($enableOsa) { " -enableOsa" } else { "" }
    $cmd += if ($executepackagedependency) { " -executepackagedependency" } else { "" }
    $cmd += if ($OsaLocationPath) { " -OsaLocationPath `"$OsaLocationPath`"" } else { "" }
    $cmd += if ($OsaFilesInclude) { " -OsaFilesInclude `"$OsaFilesInclude`"" } else { "" }
    $cmd += if ($OsaFilesExclude) { " -OsaFilesExclude `"$OsaFilesExclude`"" } else { "" }
    $cmd += if ($OsaPathExclude) { " -OsaPathExclude `"$OsaPathExclude`"" } else { "" }
    $cmd += if ($OsaArchiveToExtract) { " -OsaArchiveToExtract `"$OsaArchiveToExtract`"" } else { "" }
    $cmd += if ($OsaScanDepth) { " -OsaScanDepth $OsaScanDepth" } else { "" }    
    $cmd += if ($OSAHigh) { " -OSAHigh $OSAHigh" } else { "" }
    $cmd += if ($OSAMedium) { " -OSAMedium $OSAMedium" } else { "" }
    $cmd += if ($OSALow) { " -OSALow $OSALow" } else { "" }
    $cmd += if ($OsaReportHtml) { " -OsaReportHtml `"$OsaReportHtml`"" } else { "" }
    $cmd += if ($OsaReportPDF) { " -OsaReportPDF `"$OsaReportPDF`"" } else { "" }
    $cmd += if ($OsaJson) { " -OsaJson `"$OsaJson`"" } else { "" }
    $cmd += if ($CheckPolicy) { " -CheckPolicy `"$CheckPolicy`"" } else { "" }
    
    # Log file parameter
    $cmd += if ($Log) { " -Log `"$Log`"" } else { "" }
    
    Write-Host "$cmd"
    
    return $cmd

}

function InstallCxConsolePlugin() {
    # Full name of the plugin file
    $cliPluginFile = "$cliPlugin.zip"
	
    # URL for Checkmarx CLI Tool
    $url = "https://download.checkmarx.com/$sastVersion/Plugins/$cliPluginFile"

    # Download file
    (New-Object System.Net.WebClient).DownloadFile($url, $cliPluginFile)
    # Unzip file 
    Expand-Archive $cliPluginFile -Force

    return "$cliPlugin\$cliPlugin"
}

# ========== Execution Entry ========== #

$cliPath = InstallCxConsolePlugin
$command = "$cliPath\" + (createCommand)
Write-Host "Executing command $command"
Invoke-Expression "$command"
