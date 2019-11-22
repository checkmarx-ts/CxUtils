param(
[String]$StorageLoc="jenkins_cluster_jdk11",
[String]$JenkinsImage="jenkins/jenkins:lts-jdk11"
)

. .\scripts\common.ps1

& ".\cluster\start_cluster.ps1"

