#!/bin/sh

# Use the most recent jar based on version stamp
export CXFLOW_JAR=`ls /app/*.jar | sort -r | grep cx-flow- | head -n 1`
if [ -z $CXFLOW_JAR ]; then
    export CXFLOW_JAR=/app/cx-flow.jar
fi


echo Using CxFlow Jar: $CXFLOW_JAR
sha1sum /app/*.jar


java -Xms512m -Xmx2048m -Djava.security.egd=file:/dev/./urandom \
    -Dspring.profiles.active=web \
    $JAVA_OPTS \
    -jar $CXFLOW_JAR --$CXFLOW_MODE \
    --spring.config.location=/app/application-$CX_CONFIG.yml \
    --app=cxflow-demo-docker \
    $@ 

