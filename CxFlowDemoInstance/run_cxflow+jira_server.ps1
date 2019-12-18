param(
[String]$StorageLoc="jira-data",
[String]$Config="general",
[Switch]$Dbg,
[String]$Mode="web"
)

. .\scripts\common.ps1

$env:STORAGE_LOC = $StorageLoc
$env:JAVA_OPTS = " "
$env:CXFLOW_MODE = $Mode
$env:CX_CONFIG=$Config

if ($Dbg)
{
    $env:JAVA_OPTS = "-agentlib:jdwp=transport=dt_socket,server=y,suspend=n,address=1044"  
}

docker-compose pull cxflow-webhook jira-server
docker-compose up --build
