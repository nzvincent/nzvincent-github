#!/bin/bash

# This script create docker container / images tar files to be used to load into another docker host.
# Author: nzvincent@gmail.com | Vincent Pang

IMG=images.txt
CON=containers.txt
PS=ps-out.txt
LOG=log-migration.log
LOAD=load-script.txt
echo "" > ${LOAD}

docker images | tee ${IMG}
docker ps -as | tee ${PS}
docker ps --format "{{.ID}},{{.Image}},{{.Names}}" | tee ${CON}

echo "" >> ${LOG}
echo "`date` - Migration start " >> ${LOG}
cat ${IMG} >> ${LOG}
cat ${CON} >> ${LOG}

echo "" | tee -a ${LOG}
echo "Saving container into tar files..." | tee -a ${LOG}

while read con; do
  cid=`echo ${con} | awk -F, '{print $1}'`
  cimg=`echo ${con} | awk -F, '{print $2}'`
  cname=`echo ${con} | awk -F, '{print $3}'`

  # Convert name to lower case and migration image name and commit to images
  mname="migrate-`echo ${cname}|tr '[:upper:]' '[:lower:]'`:29dec2017"
  echo ${mname}
  #docker commit ${cname} ${mname}

  # Save images to tar files
  tarname="${mname}.tar.gz"
  echo "Saving image file to ${tarname}" | tee -a ${LOG}
  docker save ${mname} > ${tarname}
  # Generate load images
  echo "docker load < ${tarname}" | tee -a ${LOAD}
  echo "" | tee -a ${LOG}

done < ${CON}

echo "" | tee -a ${LOG}
cat ${LOAD} >> ${LOG}
echo "" | tee -a ${LOG}
docker images | tee -a ${LOG}
