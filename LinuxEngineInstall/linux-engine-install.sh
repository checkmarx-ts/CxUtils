#!/bin/bash

############################################
#Author: Justin Ruth                       #
#Version: 1.1                              #
#                                          #
####################TODOS###################
## - Add in error handling                 #
#### - cxurl isn't up                      #
#### - unzip fails                         #
#### - docker fails                        #
## - Add engine registration API calls in  #
## - Add scan API calls in                 #
############################################

############################################
#                                          #
# Configuration section                    #     
#                                          #
############################################
##CxVersion: 9.3.RC1 #######################
############################################


CxEndpointIP=
NineThreeUrl=https://download.checkmarx.com/9.3.0/CxSAST.930.Release.Setup_9.3.0.860.zip
NineThreeZipPassword=

# server.env settings to set the server.env file appropriately
# most of this should be default, just update the CxEndpoint to your CxURL and password from your manager SEE README


EnviornmentFile=server.env
EngineRunScript=run.sh
ESmessageQueueUser=cxuser
ESmessageQueuePassword=
ESmessageQueueUrl=tcp://${CxEndpointIP}:61616
ESaccessControlUrl=http://${CxEndpointIP}/CxRestAPI/auth
ESendPoint=${CxEndpointIP}:8080 
ESengineTLS=false
EsengineCertification=certificate_subject_name
EngineUnzipLocation=./cxsast-linux-engine-server/



#Usage
usage () {
  echo "Place holder for usage instructions...\n\n"
}

#Check to make sure CxManager is accessible 
CxManager_check () {
  echo "making a curl request to http://${CxEndpointIP}..."
  if [[ $(curl --silent -I http://${CxEndpointIP} | grep -E "^HTTP" | awk -F " " '{print $2}') == 200 ]];
  then
    echo "CxManager found..."
  else
    echo "curl request to CxManager failed, script halting...."
    echo "Please check the following to make sure Cxmanager is running at"
    echo ${server}
    exit
  fi
}

#Engine download section will grab 9.3 installer and rip out the windows parts
engine_download () {
  # Can refactor this once angent is decoupled from 9.3 installer
  # Currently we need to download 9.3, unzip with password to access engine.
  echo "now downloaded 9.3 agent from " ${NineThreeUrl}
  wget -O 93.zip ${NineThreeUrl}
  echo "now unziping agent"
  # unhardcode the unzip location and clean this up (password, overwrite, install dir).
  unzip -P ${NineThreeZipPassword} -o 93.zip -d ./93Install
  echo "seperating linux engine from rest of windows blah blah..."
  mv ./93Install/CxSAST.930.Release.Setup_9.3.0.860/cxsast-linux-engine-server/cxsast-engine-server-docker-image/ ${EngineUnzipLocation}
  rm -rf ./93Install
}

#engine configuration section for server.env
engine_configuration () {
  echo "Engine is downloaded and seperated from windows blah blah..."
  echo "Now configuraing engine enviornments correctly"
  echo "backing up server.env as server.old"
  cp ${EngineUnzipLocation}${EnviornmentFile} ${EngineUnzipLocation}server.old
  rm ${EngineUnzipLocation}${EnviornmentFile}
  

  echo "rewriting server.env to "${EngineUnzipLocation}${EnviornmentFile}
  echo "" > ${EngineUnzipLocation}${EnviornmentFile}
  echo "CX_ES_MESSAGE_QUEUE_USERNAME="${ESmessageQueueUser} >> ${EngineUnzipLocation}${EnviornmentFile}	
  echo "CX_ES_MESSAGE_QUEUE_PASSWORD="${ESmessageQueuePassword} >> ${EngineUnzipLocation}${EnviornmentFile}
  echo "CX_ES_MESSAGE_QUEUE_URL="${ESmessageQueueUrl} >> ${EngineUnzipLocation}${EnviornmentFile}
  echo "CX_ES_ACCESS_CONTROL_URL="${ESaccessControlUrl} >> ${EngineUnzipLocation}${EnviornmentFile}
  echo "CX_ES_END_POINT="${ESendPoint} >> ${EnviornmentFile}
  echo "CX_ENGINE_TLS_ENABLE="${ESengineTLS} >> ${EngineUnzipLocation}${EnviornmentFile}
  echo "CX_ENGINE_CERTIFICATE_SUBJECT_NAME="${EsengineCertification} >> ${EngineUnzipLocation}${EnviornmentFile}
  echo "server.env rewritten..."
  echo ""
  echo ""
  echo "These are the configurations we are using for the container..."
  cat ${EngineUnzipLocation}${EnviornmentFile}
  echo ""
  echo ""
  echo ""
}

#Starting the engine linux
engine_run_wrapper () { 
  echo "Now stoping and starting docker and running run.sh from engine download."
  service docker stop
  service docker start
  #${EngineUnzipLocation}${EngineRunScript}
  #FROM RUN.SH
  CX_SERVER_TAR=${EngineUnzipLocation}cx-engine-server.tar
  CX_SERVER_ENV=${EngineUnzipLocation}server.env
  echo loading checkmarx engine server image
  docker load < $CX_SERVER_TAR
  echo deploying checkmarx engine server container
  docker run --env-file ${EngineUnzipLocation}${EnviornmentFile} -d -p 0.0.0.0:8088:8088 cx-engine-server
  echo "Engine now running on container ID ->> "$(docker ps -qf ancestor=cx-engine-server)
  echo "Setting docker logs to console output..."
  docker logs -f $(docker ps -qf ancestor=cx-engine-server)
}


main () {
	echo "Main run goes here"
	CxManager_check
	usage
	engine_download
	engine_configuration
	engine_run_wrapper
}

main
