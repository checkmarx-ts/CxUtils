param(
[Parameter(Mandatory=$true)]
[int]$ExternalPort,
[Parameter(Mandatory=$true)]
[int]$ContainerPort,
[Parameter(Mandatory=$true)]
[String]$ImageTag,
[int]$ExternalDebugPort,
[String]$DebugBindingSpec=""
)

$Args = "run","-it","--mount","type=bind,src=${StorageLoc},target=/var/jenkins_home","-p","${ExternalPort}:${ContainerPort}"

if ($Debug)
{
    $Args += "--env", """JAVA_OPTS=-agentlib:jdwp=transport=dt_socket,server=y,suspend=n,address=${DebugBindingSpec}1044"""
    $Args += "-p", "${ExternalDebugPort}:1044"
}

$Args += "${ImageTag}"

Start-Process -NoNewWindow -Wait -FilePath docker -ArgumentList $Args
