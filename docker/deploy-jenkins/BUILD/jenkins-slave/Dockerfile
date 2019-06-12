ARG OPENJDK_VERSION

# The leading open source automation server based on Debian 

FROM openjdk:${OPENJDK_VERSION}
USER root

RUN apt-get update && apt-get install -y git python xvfb && \ 
    useradd jenkins && \
    mkdir -p /home/jenkins && \
    chown jenkins:jenkins /home/jenkins 
    
# drop back to the regular jenkins user - good practice
USER jenkins
