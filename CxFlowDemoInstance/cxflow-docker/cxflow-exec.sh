#!/bin/bash

# Use the most recent jar based on version stamp
export CXFLOW_JAR=`ls /*.jar | sort -r | head -n 1`

echo Using CxFlow Jar: $CXFLOW_JAR

java -Xms512m -Xmx2048m -Djava.security.egd=file:/dev/./urandom \
    -Dspring.profiles.active=web \
    $JAVA_OPTS \
    -jar $CXFLOW_JAR --$CXFLOW_MODE \
    --spring.config.location=/application-$CX_CONFIG.yml \
    --app=cxflow-demo-docker \
    $@ 

