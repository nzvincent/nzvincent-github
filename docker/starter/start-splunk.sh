#!/bin/bash

# Start up splunk servers

img=splunk/splunk:7.0.3

name=splunk
dir=`pwd`

docker rm -f ${name}

docker run -d -h ${name} --name ${name} \
  --restart always \
  --privileged \
  -e SPLUNK_START_ARGS=--accept-license \
  -v /etc/localtime:/etc/localtime:ro \
  -v /etc/timezone:/etc/timezone:ro \
  -v /data/DF/SHARED:/SHARED \
  -p 4001:4001 -p 8056:8056 -p 8089:8089 -p 9997:9997 -p 8000:8000 -p 8088:8088 \
  ${img}
