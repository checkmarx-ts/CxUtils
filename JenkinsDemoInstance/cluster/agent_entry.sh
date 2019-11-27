#!/bin/bash

if [ $# -gt 0 ];
then
    bash -c "$@"
else
    sleep 30s
    wget http://jenkins-master:8080/jnlpJars/agent.jar
    java $JAVA_OPTS -Djava.util.logging.config.file=/logging.properties -jar agent.jar \
        -jnlpUrl http://jenkins-master:8080/computer/$AGENT_TAG/slave-agent.jnlp \
        -workDir "/workspace" \
        || rm -f agent.jar
fi
