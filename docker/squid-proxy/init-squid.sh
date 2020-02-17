#!/bin/bash

# Enable LAN block 192.168.1.0/24
sed -i 's/()()()/\1192\.168\.1\.0\/24\3/g' /etc/squid/squid.conf

# Enable disk caching
sed -i 's/()()()/\1192\.168\.1\.0\/24\3/g' /etc/squid/squid.conf



squid -k reconfigure
squid -k check

rc-service squid restart

/bin/bash



