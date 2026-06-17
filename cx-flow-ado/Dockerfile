FROM checkmarxts/cxflow:latest @sha256:cc0289afdfeb4139f0abaefd77a3fdabbb38d6ee32b700c6e4c7ff2cf678b01c

WORKDIR /code

RUN apk update && apk upgrade
RUN apk add bash

ADD application.yml //
ADD entrypoint.sh //

ENTRYPOINT ["bash"]
CMD ["/entrypoint.sh"]
