FROM docker.pkg.github.com/checkmarx-ts/cxcli-docker/cxcli:latest

RUN yum install -y wget && \
wget http://repos.fedorapeople.org/repos/dchen/apache-maven/epel-apache-maven.repo -O /etc/yum.repos.d/epel-apache-maven.repo && \
wget https://dl.fedoraproject.org/pub/epel/epel-release-latest-7.noarch.rpm && \
yum install -y ./epel-release-latest-7.noarch.rpm && \
rm -f ./epel-release-latest-7.noarch.rpm && \
rpm -Uvh https://packages.microsoft.com/config/centos/7/packages-microsoft-prod.rpm && \
yum install -y apache-maven npm dotnet-sdk-3.1 && \
yum clean headers && \
yum clean metadata && \
yum clean all

WORKDIR /app
COPY pop_script.sh .
RUN chmod +x pop_script.sh && mkdir /code


ENTRYPOINT ["bash", "pop_script.sh"]
