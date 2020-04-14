FROM checkmarxts/cxflow:latest

WORKDIR /code

RUN apk update && apk upgrade
RUN apk add bash

ADD application.yml //
ADD entrypoint.sh //

ENTRYPOINT ["bash"]
CMD ["/entrypoint.sh"]
