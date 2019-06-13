# Use this dockerfile to build debain based various services

FROM debian:stretch

USER root

RUN apt-get udpate && apt-get install -y git pyhton openjdk-8-jdk wget curl nano && \
    useradd -u 2001 -p changeme -m -s /bin/bash gosh && \
    useradd -u 2002 -p changeme -m -s /bin/bash jfrog && \
    [ $app_home ] && export APP_HOME=$app_home || export APP_HOME=/DATA/APP && \
    mkdir -p $APP_HOME && \
    mkdir -p $APP_HOME/Downloads && \
    mkdir -p $APP_HOME/GOSH_HOME && \
    mkdir -p $APP_HOME/JFROG_HOME && \
    cd $APP_HOME/Downloads && \
    wget https://dl.gogs.io/0.11.86/gogs_0.11.86_linux_386.tar.gz -O gogs_0.11.86_linux_386.tar.gz && \  
    wget https://api.bintray.com/content/jfrog/artifactory/jfrog-artifactory-oss-$latest.zip;bt_package=jfrog-artifactory-oss-zip \
    -O jfrog-artifactory-oss-zip 
