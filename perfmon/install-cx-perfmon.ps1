<#
.SYNOPSIS
Installs / Uninstalls Perfmon Data Collector Sets for monitoring performance of Checkmarx infrastructure.
.VERSION
V1 - 13 APR 2020 - Initial version
.AUTHOR
Benjamin Stokes (ben.stokes@checkmarx.com)
#>


[CmdletBinding()]
param (
  [Parameter(Mandatory = $False)] [switch] $Uninstall
)

# Define bare minimum counters for an overall view of the machine.
$cxsast_manager_overview = @(
    "\Process(_Total)\% Processor Time",
    "\System\Processor Queue Length",
    "\PhysicalDisk(_Total)\Current Disk Queue Length",
    "\PhysicalDisk(_Total)\Avg. Disk Queue Length",
    "\Memory\Page Faults/sec",
    "\Memory\Page Reads/sec",
    "\LogicalDisk(C:)\% Free Space",
    "\LogicalDisk(C:)\Free Megabytes",
    "\Paging File(\??\C:\pagefile.sys)\% Usage",
    "\Paging File(\??\C:\pagefile.sys)\% Usage Peak"
)

# Define CPU related counters for the manager server
$cxsast_manager_cpu = @(
    "\Process(_Total)\% Processor Time",
    "\Process(CxAudit)\% Processor Time",
    "\Process(CxJobsManagerWinService)\% Processor Time",
    "\Process(CxScansManagerWinService)\% Processor Time",
    "\Process(CxSourceAnalyzerEngine.WinService)\% Processor Time",
    "\Process(CxSystemManagerService)\% Processor Time",
    "\Process(java)\% Processor Time",
    "\Process(tomcat8)\% Processor Time",
    "\Process(w3wp)\% Processor Time",
    "\Process(w3wp#1)\% Processor Time",
    "\Process(w3wp#2)\% Processor Time",
    "\Processor Information(_Total)\% Privileged Time",
    "\Processor Information(_Total)\% Processor Time",
    "\Processor Information(_Total)\% User Time",
    "\System\Processor Queue Length"
)

# Define disk related counters for the manager server
$cxsast_manager_disk = @(
    "\LogicalDisk(_Total)\Disk Read Bytes/sec",
    "\LogicalDisk(_Total)\Disk Reads/sec",
    "\Memory\Committed Bytes",
    "\PhysicalDisk(_Total)\% Disk Time",
    "\PhysicalDisk(_Total)\Avg. Disk Bytes/Read",
    "\PhysicalDisk(_Total)\Avg. Disk Queue Length",
    "\PhysicalDisk(_Total)\Avg. Disk sec/Read",
    "\PhysicalDisk(_Total)\Current Disk Queue Length",
    "\PhysicalDisk(_Total)\Disk Read Bytes/sec",
    "\PhysicalDisk(_Total)\Disk Reads/sec",
    "\PhysicalDisk(_Total)\Disk Transfers/sec",
    "\Processor Information(_Total)\% Processor Time",
    "\LogicalDisk(C:)\% Free Space",
    "\LogicalDisk(C:)\Free Megabytes",
    "\Paging File(\??\C:\pagefile.sys)\% Usage",
    "\Paging File(\??\C:\pagefile.sys)\% Usage Peak"
)

# Define memory related counters for the manager server
$cxsast_manager_memory = @(
    "\Memory\Committed Bytes",
    "\Memory\Page Faults/sec",
    "\Memory\Page Reads/sec",
    "\Memory\Page Writes/sec",
    "\Memory\Pages Input/sec",
    "\Memory\Pages Output/sec",
    "\Memory\Pages/sec",
    "\Process(_Total)\Page Faults/sec",
    "\Process(_Total)\Working Set",
    "\Process(CxAudit)\Page Faults/sec",
    "\Process(CxAudit)\Working Set",
    "\Process(CxJobsManagerWinService)\Page Faults/sec",
    "\Process(CxJobsManagerWinService)\Working Set",
    "\Process(CxScansManagerWinService)\Page Faults/sec",
    "\Process(CxScansManagerWinService)\Working Set",
    "\Process(CxSourceAnalyzerEngine.WinService)\Page Faults/sec",
    "\Process(CxSourceAnalyzerEngine.WinService)\Working Set",
    "\Process(CxSystemManagerService)\Page Faults/sec",
    "\Process(CxSystemManagerService)\Working Set",
    "\Process(tomcat8)\Page Faults/sec",
    "\Process(tomcat8)\Working Set",
    "\Process(w3wp)\Page Faults/sec",
    "\Process(w3wp)\Working Set",
    "\Process(w3wp#1)\Page Faults/sec",
    "\Process(w3wp#1)\Working Set",
    "\Process(w3wp#2)\Page Faults/sec",
    "\Process(w3wp#2)\Working Set",
    "\Processor Information(_Total)\% Processor Time"
)

# Define dotnet application related counters for the manager server
$cxsast_manager_dotnet = @(
    "\ASP.NET Apps v4.0.30319(_LM_W3SVC_1_ROOT_CxRestAPI)\Request Execution Time",
    "\ASP.NET Apps v4.0.30319(_LM_W3SVC_1_ROOT_CxRestAPI)\Request Wait Time",
    "\ASP.NET Apps v4.0.30319(_LM_W3SVC_1_ROOT_CxRestAPI)\Requests Executing",
    "\ASP.NET Apps v4.0.30319(_LM_W3SVC_1_ROOT_CxRestAPI)\Requests In Application Queue",
    "\ASP.NET Apps v4.0.30319(_LM_W3SVC_1_ROOT_CxRestAPI)\Requests Timed Out",
    "\ASP.NET Apps v4.0.30319(_LM_W3SVC_1_ROOT_CxRestAPI)\Requests/Sec",
    "\ASP.NET Apps v4.0.30319(_LM_W3SVC_1_ROOT_CxWebClient)\Request Execution Time",
    "\ASP.NET Apps v4.0.30319(_LM_W3SVC_1_ROOT_CxWebClient)\Request Wait Time",
    "\ASP.NET Apps v4.0.30319(_LM_W3SVC_1_ROOT_CxWebClient)\Requests Executing",
    "\ASP.NET Apps v4.0.30319(_LM_W3SVC_1_ROOT_CxWebClient)\Requests Failed",
    "\ASP.NET Apps v4.0.30319(_LM_W3SVC_1_ROOT_CxWebClient)\Requests In Application Queue",
    "\ASP.NET Apps v4.0.30319(_LM_W3SVC_1_ROOT_CxWebClient)\Requests Timed Out",
    "\ASP.NET Apps v4.0.30319(_LM_W3SVC_1_ROOT_CxWebClient)\Requests/Sec",
    "\ASP.NET Apps v4.0.30319(_LM_W3SVC_1_ROOT_CxWebClient)\Sessions Active",
    "\ASP.NET Apps v4.0.30319(_LM_W3SVC_1_ROOT_CxWebInterface)\Request Execution Time",
    "\ASP.NET Apps v4.0.30319(_LM_W3SVC_1_ROOT_CxWebInterface)\Request Wait Time",
    "\ASP.NET Apps v4.0.30319(_LM_W3SVC_1_ROOT_CxWebInterface)\Requests Executing",
    "\ASP.NET Apps v4.0.30319(_LM_W3SVC_1_ROOT_CxWebInterface)\Requests Failed",
    "\ASP.NET Apps v4.0.30319(_LM_W3SVC_1_ROOT_CxWebInterface)\Requests In Application Queue",
    "\ASP.NET Apps v4.0.30319(_LM_W3SVC_1_ROOT_CxWebInterface)\Requests Succeeded",
    "\ASP.NET Apps v4.0.30319(_LM_W3SVC_1_ROOT_CxWebInterface)\Requests/Sec",
    "\Processor Information(_Total)\% Processor Time"
)

# Create our data collector sets
# See https://docs.microsoft.com/en-us/windows-server/administration/windows-commands/logman-create-counter for logman command line arg documentation
function create_datacollectors() {
    Write-Host "Creating Perfmon Data Collector Sets"
    md "C:\PerfLogs\Admin" -Force | out-null

    Write-Host "Creating cxsast_manager_overview"
    logman create counter cxsast_manager_overview -c $($cxsast_manager_overview) -max $max_log_size_in_mb -si $sample_interval_in_seconds -v $log_file_version_mask -o "C:\PerfLogs\Admin\cxsast_manager_overview\cxsast_manager_overview"

    Write-Host "Creating cxsast_manager_cpu"
    logman create counter cxsast_manager_cpu -c $($cxsast_manager_cpu) -max $max_log_size_in_mb -si $sample_interval_in_seconds -v $log_file_version_mask -o "C:\PerfLogs\Admin\cxsast_manager_cpu\cxsast_manager_cpu"

    Write-Host "Creating cxsast_manager_disk"
    logman create counter cxsast_manager_disk -c $($cxsast_manager_disk) -max $max_log_size_in_mb -si $sample_interval_in_seconds -v $log_file_version_mask -o "C:\PerfLogs\Admin\cxsast_manager_disk\cxsast_manager_disk"

    Write-Host "Creating cxsast_manager_memory"
    logman create counter cxsast_manager_memory -c $($cxsast_manager_memory) -max $max_log_size_in_mb -si $sample_interval_in_seconds -v $log_file_version_mask -o "C:\PerfLogs\Admin\cxsast_manager_memory\cxsast_manager_memory"

    Write-Host "Creating cxsast_manager_dotnet"
    logman create counter cxsast_manager_dotnet -c $($cxsast_manager_dotnet) -max $max_log_size_in_mb -si $sample_interval_in_seconds -v $log_file_version_mask -o "C:\PerfLogs\Admin\cxsast_manager_dotnet\cxsast_manager_dotnet"
}

# Create scheduled tasks to run our data collector sets
function create_tasks() {
    Write-Host "Creating nightly scheduled tasks to manage data collection sets"
    SCHTASKS /Create /TN "perfmon-cxsast_manager_overview-Nightly" /F /SC HOURLY /ST 00:00 /RU SYSTEM /TR "powershell.exe -command logman stop cxsast_manager_overview; logman start cxsast_manager_overview; dir c:\PerfLogs\Admin\cxsast_manager_overview\*.blg |?{ $_.LastWriteTime -lt (Get-Date).AddDays(-7)} | del" | Write-Verbose
    SCHTASKS /Create /TN "perfmon-cxsast_manager_cpu-Nightly" /F /SC HOURLY /ST 00:00 /RU SYSTEM /TR "powershell.exe -command logman stop cxsast_manager_cpu; logman start cxsast_manager_cpu; dir c:\PerfLogs\Admin\cxsast_manager_cpu\*.blg |?{ $_.LastWriteTime -lt (Get-Date).AddDays(-7)} | del" | Write-Verbose
    SCHTASKS /Create /TN "perfmon-cxsast_manager_disk-Nightly" /F /SC HOURLY /ST 00:00 /RU SYSTEM /TR "powershell.exe -command logman stop cxsast_manager_disk; logman start cxsast_manager_disk; dir c:\PerfLogs\Admin\cxsast_manager_disk\*.blg |?{ $_.LastWriteTime -lt (Get-Date).AddDays(-7)} | del" | Write-Verbose
    SCHTASKS /Create /TN "perfmon-cxsast_manager_memory-Nightly" /F /SC HOURLY /ST 00:00 /RU SYSTEM /TR "powershell.exe -command logman stop cxsast_manager_memory; logman start cxsast_manager_memory; dir c:\PerfLogs\Admin\cxsast_manager_memory\*.blg |?{ $_.LastWriteTime -lt (Get-Date).AddDays(-7)} | del" | Write-Verbose
    SCHTASKS /Create /TN "perfmon-cxsast_manager_dotnet-Nightly" /F /SC HOURLY /ST 00:00 /RU SYSTEM /TR "powershell.exe -command logman stop cxsast_manager_dotnet; logman start cxsast_manager_dotnet; dir c:\PerfLogs\Admin\cxsast_manager_dotnet\*.blg |?{ $_.LastWriteTime -lt (Get-Date).AddDays(-7)} | del" | Write-Verbose
    
    Write-Host "Creating startup scheduled tasks to manage data collection sets"
    SCHTASKS /Create /TN "perfmon-cxsast_manager_overview-Startup" /F /SC ONSTART /RU SYSTEM /TR "logman start cxsast_manager_overview" | Write-Verbose
    SCHTASKS /Create /TN "perfmon-cxsast_manager_cpu-Startup" /F /SC ONSTART /RU SYSTEM /TR "logman start cxsast_manager_cpu" | Write-Verbose
    SCHTASKS /Create /TN "perfmon-cxsast_manager_disk-Startup" /F /SC ONSTART /RU SYSTEM /TR "logman start cxsast_manager_disk" | Write-Verbose
    SCHTASKS /Create /TN "perfmon-cxsast_manager_memory-Startup" /F /SC ONSTART /RU SYSTEM /TR "logman start cxsast_manager_memory" | Write-Verbose
    SCHTASKS /Create /TN "perfmon-cxsast_manager_dotnet-Startup" /F /SC ONSTART /RU SYSTEM /TR "logman start cxsast_manager_dotnet" | Write-Verbose   
}

function delete_tasks() {
    Write-Host "Deleting nightly scheduled tasks to manage data collection sets"
    SCHTASKS /delete /TN "perfmon-cxsast_manager_overview-Nightly" /f
    SCHTASKS /delete /TN "perfmon-cxsast_manager_cpu-Nightly" /f
    SCHTASKS /delete /TN "perfmon-cxsast_manager_disk-Nightly" /f
    SCHTASKS /delete /TN "perfmon-cxsast_manager_memory-Nightly" /f
    SCHTASKS /delete /TN "perfmon-cxsast_manager_dotnet-Nightly" /f

    Write-Host "Deleting startup scheduled tasks to manage data collection sets"
    SCHTASKS /delete /TN "perfmon-cxsast_manager_overview-Startup" /f
    SCHTASKS /delete /TN "perfmon-cxsast_manager_cpu-Startup" /f
    SCHTASKS /delete /TN "perfmon-cxsast_manager_disk-Startup" /f
    SCHTASKS /delete /TN "perfmon-cxsast_manager_memory-Startup" /f
    SCHTASKS /delete /TN "perfmon-cxsast_manager_dotnet-Startup" /f
}


# Start the collector sets running via their scheduled task
function run_tasks() {
    Write-Host "Running tasks once to start them up"
    SCHTASKS /Run /TN perfmon-cxsast_manager_overview-Startup | Write-Verbose
    SCHTASKS /Run /TN perfmon-cxsast_manager_cpu-Startup | Write-Verbose
    SCHTASKS /Run /TN perfmon-cxsast_manager_disk-Startup | Write-Verbose
    SCHTASKS /Run /TN perfmon-cxsast_manager_memory-Startup | Write-Verbose
    SCHTASKS /Run /TN perfmon-cxsast_manager_dotnet-Startup | Write-Verbose
}

# Delete any data collector sets
function delete_datacollectors() { 
    Write-Host "Deleting data collector sets"

    Write-Host "Deleting cxsast_manager_overview"
    logman stop cxsast_manager_overview | out-null
    logman delete cxsast_manager_overview | Write-Verbose

    Write-Host "Deleting cxsast_manager_cpu"
    logman stop cxsast_manager_cpu | out-null
    logman delete cxsast_manager_cpu | Write-Verbose

    Write-Host "Deleting cxsast_manager_disk"
    logman stop cxsast_manager_disk | out-null
    logman delete cxsast_manager_disk | Write-Verbose

    Write-Host "Deleting cxsast_manager_memory"
    logman stop cxsast_manager_memory | out-null
    logman delete cxsast_manager_memory | Write-Verbose

    Write-Host "Deleting cxsast_manager_dotnet"
    logman stop cxsast_manager_dotnet | out-null
    logman delete cxsast_manager_dotnet | Write-Verbose
}


function uninstall() {
  Write-Host "Uninstalling..."
  delete_tasks
  delete_datacollectors
}

function install() {
  Write-Host "Installing..."
  create_datacollectors
  create_tasks
  run_tasks
}

if ($Uninstall.IsPresent) {
  uninstall
} else {
  install
}

Write-Host "Finished."
