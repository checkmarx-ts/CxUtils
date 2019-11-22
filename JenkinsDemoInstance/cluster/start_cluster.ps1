

$env:JENKINS_IMAGE = $JenkinsImage
$env:STORAGE_LOC = $StorageLoc

docker-compose -f cluster/docker-compose.yml up --build


