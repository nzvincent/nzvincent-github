#!/bin/bash

docker  rm -f splunkf

docker run --name splunkf --hostname splunkf -d \
  --restart always \
  --privileged \
  -e "SPLUNK_START_ARGS=--accept-license --seed-passwd changeme" \
  -v /etc/localtime:/etc/localtime:ro \
  -v /etc/timezone:/etc/timezone:ro \
  -v /data/DF/SHARED:/SHARED \
  splunk/universalforwarder:7.1.2
