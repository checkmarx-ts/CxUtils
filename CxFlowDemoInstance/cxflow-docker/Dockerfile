FROM checkmarxts/cxflow:latest

COPY cxflow-exec.sh /cxflow-exec.sh
COPY *.yml /

RUN chmod +x /cxflow-exec.sh && \
chmod 644 /*.yml

ENTRYPOINT ["/cxflow-exec.sh"]


