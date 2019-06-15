#!/bin/bash

# @Usage: ./samba-docker-image.sh
# @Author: nzvincent@gmail.com
# @Ref: https://hub.docker.com/r/dperson/samba/
# @Notes: This standing up a Samba server for Windows files sharing

IMAGE=jenserat/samba-publicshare
NAME=samba
HOST=${name^^}

RUN_OPT="-td"
PORTMAP="-p 445:445 -p 137:137 -p 138:138 -p 139:139"
VOLUME="-v ~/WORKSPACE:/srv -v `pwd`/CONFIG:/etc/samba \"
EXTRA_OPT=""

if [ $1 = "force" ];
  docker rm -f samba
fi

docker run ${RUN_OPT} \
  --name ${NAME} \
  -h ${HOST} ${PORTMAP} ${VOLUME} ${EXTRA_OPT} \
	${IMAGE}
