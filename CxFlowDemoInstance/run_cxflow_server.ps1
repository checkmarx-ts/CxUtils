param(
[String]$Config="general",
[Switch]$Dbg
)


$env:JAVA_OPTS = " "
$env:CXFLOW_MODE = "web"
$env:CX_CONFIG=$Config

if ($Dbg)
{
    $env:JAVA_OPTS = "-agentlib:jdwp=transport=dt_socket,server=y,suspend=n,address=1044"  
}

docker-compose pull cxflow-webhook
docker-compose -f docker-compose-cxflow-server.yml up --build
