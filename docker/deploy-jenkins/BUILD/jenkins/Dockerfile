ARG JENKINS_VERSION

# The leading open source automation server based on Debian 

FROM jenkins/jenkins:${JENKINS_VERSION}

USER root

COPY executors.groovy /usr/share/jenkins/ref/init.groovy.d/executors.groovy

RUN apt-get update && apt-get install -y git python && \
    chown jenkins:jenkins /usr/share/jenkins/ref/init.groovy.d/executors.groovy

# drop back to the regular jenkins user - good practice
USER jenkins
