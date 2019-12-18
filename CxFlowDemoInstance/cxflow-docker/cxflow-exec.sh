#!/bin/bash

export CXFLOW_JAR=`ls /*.jar`

java -Xms512m -Xmx2048m -Djava.security.egd=file:/dev/./urandom \
    -Dspring.profiles.active=web \
    $JAVA_OPTS \
    -jar $CXFLOW_JAR --$CXFLOW_MODE \
    --spring.config.location=/application-$CX_CONFIG.yml \
    --app=cxflow-demo-docker \
    $@ 

