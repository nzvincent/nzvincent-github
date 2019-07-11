#!/bin/bash

#  Stand up a host based squid proxy server ( --net=host )
# Author: nzvincent@gmail.com

img=debian:jessie
img=debian-squid:homebrew

name=squid
dir=`pwd`


docker rm -f ${name}

docker run -it -h ${name} --name ${name} \
  --restart always \
  --privileged \
  -v /etc/localtime:/etc/localtime \
  -v /etc/timezone:/etc/timezone \
  -v ${dir}/CONFIG/cache:/var/cache/squid \
  -v ${dir}/CONFIG/log:/var/log/squid \
  --net=host \
  ${img} \
  /bin/sh


# mount 2g to tmpfs to avoid firefox crashing.
# default is 64M
#        --mount type=tmpfs,dst=/dev/shm,tmpfs-size=1g \
#    OR --shm-size 2g
#  If above command not supported, login to the container to change the memory size OR include this in the entrypoint.sh file
#  mount -o remount,size=2G /dev/shm


# /etc/squid/squid.conf

