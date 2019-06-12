ARG JENKIN_VERSION
ARG JENKIN_APT_GET

FROM jenkins/jenkins:${JENKIN_VERSION}

USER root
RUN apt-get update && apt-get install -y git ${JENKIN_APT_GET}

# drop back to the regular jenkins user - good practice
USER jenkins
