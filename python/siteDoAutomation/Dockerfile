FROM debian:stretch

# Things you need to run python selenium with firefox webdriver
# @Author: nzvincent@gmail.com | Vincent Pang


ENV USER=pytester
ENV UID=2000
ENV GID=2000

COPY requirements.txt .

RUN apt-get update && apt-get upgrade && \
    apt-get -y install sudo git python python-dev python-pip wget curl git nano vim firefox-esr openssh-server nginx && \
    adduser --disabled-password --gecos "" "$USER" && \
    wget https://github.com/mozilla/geckodriver/releases/download/v0.24.0/geckodriver-v0.24.0-linux64.tar.gz && \
    tar xzf geckodriver-v0.24.0-linux64.tar.gz && \
    chmod 755 geckodriver && \
    cp geckodriver /usr/bin/ && \
    su - "$USER" && \
    pip install -r requirements.txt

  
