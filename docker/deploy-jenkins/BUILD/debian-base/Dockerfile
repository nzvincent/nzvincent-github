# Use this dockerfile to build debain based various services

FROM debian:stretch

USER root

RUN apt-get udpate && apt-get install -y git pyhton wget curl nano && \
    useradd jenkins && \
    useradd gogsh && \
    useradd jfrog && \
    useradd tomcat && \
    [ -z app_home ] && export APP_HOME=$app_home || export APP_HOME=/DATA/APP && \
    mkdir -p $APP_HOME && \
    mkdir -p $APP_HOME/GOGS_HOME && \
    mkdir -p $APP_HOME/JFROG_HOME && \
    mkdir -p $APP_HOME/TOMCAT_HOME && \
    wget ??Source -O $APP_HOME/GOGS_HOME/gogs.file && \
    wget ??Source -O $APP_HOME/JFROGHOME/gogs.file && \
    wget ??Source -O $APP_HOME/TOMCAT_HOME/gogs.file && 
