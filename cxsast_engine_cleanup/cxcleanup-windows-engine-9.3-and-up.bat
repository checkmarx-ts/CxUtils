REM For EngineServiceScans - modify path according to CX_ES_ENGINE_SCANS_PARENT_PATH environment variable

ECHO Removing engine scan files older than 7 days...
forfiles -p C:\EngineServiceScans\Scans\ -s -m *.* /D -7  /C "cmd /c del /f @PATH"

ECHO Done!