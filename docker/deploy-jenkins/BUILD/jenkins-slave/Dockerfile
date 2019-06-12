ARG JENKIN_SLAVE_OPENJDK_VERSION
ARG JENKIN_SLAVE_APT_GET

# The leading open source automation server based on Debian 

FROM openjdk:${JENKIN_SLAVE_OPENJDK_VERSION}

USER root
RUN apt-get update && apt-get install -y git ${JENKIN_APT_GET}

# drop back to the regular jenkins user - good practice
USER jenkins
