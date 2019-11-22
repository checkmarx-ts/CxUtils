#!/bin/bash

if [ $# -gt 0 ];
then
    bash -c "$@"
else
    wget http://jenkins-master:8080/jnlpJars/agent.jar
    java $JAVA_OPTS -jar agent.jar \
        -jnlpUrl http://jenkins-master:8080/computer/$AGENT_TAG/slave-agent.jnlp \
        -workDir "/workspace" \
        -loggingConfig /logging.properties \
        || rm -f agent.jar
fi
