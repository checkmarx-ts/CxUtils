param(
[String]$StorageLoc="jenkins_cluster_jdk8",
[String]$JenkinsImage="jenkins/jenkins:lts"
)

. .\scripts\common.ps1

& ".\cluster\start_cluster.ps1"


