@echo off;
REM Add parameter -report_type '%2' if any report type other than PDF is required.  Other options are CSV, RTF or XML.
powershell.exe -ExecutionPolicy Bypass "& '.\SAST-Create-Report.ps1' -sast_url '%1'