ARG JENKIN_VERSION

FROM jenkins/jenkins:${JENKIN_VERSION}

USER root
RUN apt-get update && apt-get install -y git ansible

# drop back to the regular jenkins user - good practice
USER jenkins
