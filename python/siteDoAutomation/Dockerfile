FROM debian:latest

ENV USER=pytester
ENV UID=2000
ENV GID=2000

RUN apt-get update && apt-get upgrade && \
    apt-get -y install sudo git python python-dev python-pip wget curl git nano vi && \
    adduser --disabled-password --gecos "" "$USER" && \
    wget https://github.com/mozilla/geckodriver/releases/download/v0.24.0/geckodriver-v0.24.0-linux64.tar.gz && \
    tar xzf geckodriver-v0.24.0-linux64.tar.gz && \
    chmod 755 geckodriver && \
    cp geckodriver /usr/bin/ && \
    su - "$USER" && \
    pip install selenium requests cryptography \

    
