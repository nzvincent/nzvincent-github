#!/bin/bash

# This is docker container starter script template
# @author: nzvincent@gmail.com

# Modify images and target container name ( use lower case )
img=centos:updated-v1
name=starter

dir=`pwd`
BASE=/data/DF/HOSTS/${name^^}
SHARED=/data/DF/SHARED/${name}
ENVFILE=/etc/environment
TZONE="-v /etc/timezone:/etc/timezone -v /etc/localtime:/etc/localtime"
LOGFILE=${SHARED}/logfile-${name}.txt

echo "`date` - Starting up $0 $@" | tee -a ${LOGFILE}

if [ ! -d ${SHARED} ]; then
  mkdir -p ${SHARED} | tee -a ${LOGFILE}
fi

if [ $1 = "force" ]; then
  docker rm -f ${name} | tee -a ${LOGFILE}
fi

CMD="docker run -it -h ${name} --name ${name} \
  --restart always \
  --privileged \
  -v ${SHARED}:/SHARED \
  -v ${ENVFILE}:/etc/environment \
  ${TZONE} \
  ${img}"

echo ${CMD} | tee -a ${LOGFILE}
${CMD}

