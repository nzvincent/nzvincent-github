#!/bin/bash

img=registry:2
name=registry
dir=`pwd`


# Usage:
# Place LetsEncrypt generated fullchain and key here:
#  - CERTS/fullchain.cer
#  - CERTS/yourdomain.key
#  - REG_IMAGE
# Docker tag
#   docker tag your-image:latest your-domain.com/your-image
# Docker push 
#   docker push your-domain.com/your-image
# Registry from URI
#   https://your-domain.com/v2
#   https://your-domain.com/v2/_catalog



if [ $1 = "rebuild" ]; then
  docker rm -f ${name}
fi

docker run -d -h ${name} --name ${name} \
  --restart always \
  --privileged \
  -v /etc/localtime:/etc/localtime:ro \
  -v /etc/timezone:/etc/timezone:ro \
  -v `pwd`/CERTS:/certs \
  -v `pwd`/REG_IMAGES:/var/lib/registry \
  -e REGISTRY_HTTP_ADDR=0.0.0.0:443 \
  -e REGISTRY_HTTP_TLS_CERTIFICATE=/certs/fullchain.cer \
  -e REGISTRY_HTTP_TLS_KEY=/certs/domain.key \
  -p 443:443 \
  ${img}


