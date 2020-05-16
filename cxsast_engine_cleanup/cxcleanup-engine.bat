REM For CxEngine Servers - modify paths according to Cx installation folders

ECHO Removing engine scan files older than 7 days...
forfiles -p "C:\Program Files\Checkmarx\Checkmarx Engine Server\Engine Server\Scans" -s -m *.* /D -7  /C "cmd /c del /F @path"
forfiles -p "C:\Program Files\Checkmarx\Checkmarx Engine Server\Engine Server\Logs\ScanLogs" -s -m *.* /D -7  /C "cmd /c del /F @path"

ECHO Done!