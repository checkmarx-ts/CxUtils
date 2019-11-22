param(
[String]$StorageLoc="jenkins_standalone_jdk8",
[int]$Port=8080,
[switch]$Debug,
[String]$JenkinsImage="jenkins/jenkins:lts"
)

. .\scripts\common.ps1

$debugPort = 1048

& ".\scripts\run_jenkins_standalone.ps1" -ExternalPort $Port -ContainerPort 8080 `
    -ImageTag $JenkinsImage -ExternalDebugPort $debugPort

