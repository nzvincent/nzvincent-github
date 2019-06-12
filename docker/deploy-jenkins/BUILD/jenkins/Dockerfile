ARG JENKINS_VERSION
ARG JENKINS_APT_GET

# The leading open source automation server based on Debian 

FROM jenkins/jenkins:${JENKINS_VERSION}

COPY executors.groovy /usr/share/jenkins/ref/init.groovy.d/executors.groovy

USER root
RUN apt-get update && apt-get install -y ${JENKINS_APT_GET}

# drop back to the regular jenkins user - good practice
USER jenkins
