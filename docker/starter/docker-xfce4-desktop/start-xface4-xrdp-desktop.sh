#!/bin/bash

# This script start up xrdp on container start
# Notes: It's a working copy

name=desktop-tv1
img=debian-xfce4:ready5


if [ $1 = "force" ]; then
  docker rm -f ${name}
fi

# mount 2g to tmpfs to avoid firefox crashing.
# default is 64M
#        --mount type=tmpfs,dst=/dev/shm,tmpfs-size=1g \
#    OR --shm-size 2g
#  If above command not supported, login to the container to change the memory size OR include this in the entrypoint.sh file
#  mount -o remount,size=2G /dev/shm

docker run -di --name ${name} -h ${name} \
        --privileged --restart always \
        -v /data:/SHARED \
        -v /etc/timezone:/etc/timezone \
        -v /etc/localtime:/etc/localtime \
        -v `pwd`/ENV/resolv.conf:/etc/resolv.conf \
        -v `pwd`/ENV/environment:/etc/environment \
        -v `pwd`/ENV/hostsfile:/etc/hostsfile \
        -v `pwd`/ENV/entrypoint.sh:/root/entrypoint.sh \
        -p 8000:3389 -p 2222:22  ${img} \
        /root/entrypoint.sh


sleep 2

docker logs ${name}

sleep 2
docker ps -a

