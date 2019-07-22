#!/bin/bash


# mount 2g to tmpfs to avoid firefox crashing.
# default is 64M
#        --mount type=tmpfs,dst=/dev/shm,tmpfs-size=1g \
#    OR --shm-size 2g
#  If above command not supported, login to the container to change the memory size OR include this in the entrypoint.sh file
#  mount -o remount,size=2G /dev/shm


echo "Append hosts and add environment variables"
cat /etc/hostsfile >> /etc/hosts
source /etc/environment

echo "Avoid Firefox crashing..."
mount -o remount,size=2G /dev/shm

echo "Starting up entrypoint script"


/etc/init.d/xrdp stop

rm /var/run/xrdp/*.pid

/etc/init.d/xrdp stop
/etc/init.d/xrdp start
