@echo off;

powershell.exe -ExecutionPolicy Bypass "& '.\SAST-Create-CSV-Report.ps1' -sast_url '%1' -overwrite_existing_report" 