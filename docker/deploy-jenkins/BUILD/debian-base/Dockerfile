# Use this dockerfile to build debain based various services

FROM debian:stretch

RUN apt-get udpate && apt-get install -y git pyhton && \
    useradd jenkins && \
    useradd gogsh && \
    useradd jfrog && \
    useradd tomcat

