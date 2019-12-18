param(
[String]$StorageLoc="jira_data",
[String]$Config="general",
[Switch]$Dbg
)

. .\scripts\common.ps1

$env:STORAGE_LOC = $StorageLoc
$env:JAVA_OPTS = " "
$env:CXFLOW_MODE = "web"
$env:CX_CONFIG=$Config

if ($Dbg)
{
    $env:JAVA_OPTS = "-agentlib:jdwp=transport=dt_socket,server=y,suspend=n,address=1044"  
}

docker-compose pull cxflow-webhook jira-server
docker-compose up --build
