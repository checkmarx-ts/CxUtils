param(
[String]$StorageLoc="jenkins_standalone_jdk11",
[int]$Port=8080,
[switch]$Debug,
[String]$JenkinsImage="jenkins/jenkins:lts-jdk11"
)

. .\scripts\common.ps1

$debugPort = 1041

& ".\scripts\run_jenkins_standalone.ps1" -ExternalPort $Port -ContainerPort 8080 `
    -ImageTag $JenkinsImage -ExternalDebugPort $debugPort -DebugBindingSpec "*:"

