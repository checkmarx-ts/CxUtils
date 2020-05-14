param(
[String]$Config="general",
[Parameter(Mandatory=$true)]
[String]$JiraURL,
[Parameter(Mandatory=$true)]
[String]$CxProject,
[Parameter(Mandatory=$true)]
[String]$Src,
[Switch]$Dbg
)

$env:JAVA_OPTS = " "

if ($Dbg)
{
    $env:JAVA_OPTS = "-agentlib:jdwp=transport=dt_socket,server=y,suspend=n,address=1044"  
}

docker build -t cxflow-local cxflow-docker
docker run -it -v ${Src}:/scratch -p 1039:1044 --env CXFLOW_MODE=scan --env CX_CONFIG=$Config --env JAVA_OPTS=$env:JAVA_OPTS cxflow-local --jira.url=$JiraURL --f=/scratch --cx-project=$CxProject
