FROM checkmarxts/cxflow:latest


COPY cxflow-exec.sh /cxflow-exec.sh

# Drop any cxflow jar in and rebuild for development debugging purposes.
# A jar stamped with a later version or no version will be used instead
# of the jar published in "checkmarxts/cxflow:latest".
COPY *.yml cx-flow*.jar /

RUN chmod +x /cxflow-exec.sh && \
chmod 644 /application-*.yml && \
mkdir /scratch

ENTRYPOINT ["/cxflow-exec.sh"]


