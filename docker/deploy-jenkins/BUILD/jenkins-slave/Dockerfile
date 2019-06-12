ARG JENKINS_SLAVE_OPENJDK_VERSION
ARG JENKIN_SLAVE_APT_GET

# The leading open source automation server based on Debian 

FROM openjdk:${JENKINS_SLAVE_OPENJDK_VERSION}
USER root

RUN apt-get update && apt-get install -y ${JENKIN_SLAVE_APT_GET} && \ 
    useradd -U -g 1000 -u 1000 -m /home/jenkins -l -s /bin/bash jenkins && \
    mkdir -p /home/jenkins & chown jenkins:jenkins /home/jenkins 
    
# drop back to the regular jenkins user - good practice
USER jenkins
