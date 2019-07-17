#!/bin/bash

img=elastic/apm-server:6.5.1

name=apm
dir=`pwd`

docker rm -f ${name}

docker run -d -h ${name} --name ${name} \
  --restart always \
  --privileged \
  --mount type=bind,source="$(pwd)"/apm-server.yml,target=/usr/share/apm-server/apm-server.yml \
  -v /etc/localtime:/etc/localtime \
  -v /etc/timezone:/etc/timezone \
  -p 8200:8200 \
  ${img}

