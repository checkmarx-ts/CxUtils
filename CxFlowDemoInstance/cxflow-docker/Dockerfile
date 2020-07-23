FROM checkmarx/cx-flow:latest


COPY cxflow-exec.sh /cxflow-exec.sh

# Groovy scripts (files ending in ".groovy") are copied into the /app directory.  
# Reference groovy scripts as full path or relative to the cx-flow jar.

# Drop any cxflow jar in and rebuild for development debugging purposes.
# A jar stamped with a later version or no version will be used instead
# of the jar published in "checkmarxts/cxflow:latest".
COPY *.yml *.groovy cx-flow*.jar /app/

RUN chmod +x /cxflow-exec.sh && \
chmod 644 /app/application-*.yml && \
mkdir /scratch

ENTRYPOINT ["/cxflow-exec.sh"]


