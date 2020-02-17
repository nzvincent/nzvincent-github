#!/bin/bash

# Enable LAN block 192.168.1.0/24
sed -i 's/()()()/\1192\.168\.1\.0\/24\3/g' /etc/squid/squid.conf

# Enable disk caching
# FROM: #cache_dir ufs /var/cache/squid 100 16 256
#   TO: cache_dir ufs /var/cache/squid 7000 16 256
sed -i 's/^\#cache_dir\(\sufs\s\/var\/cache\/squid\s\)\(100\)\(.*\)/cache_dir\17000\3/g' /etc/squid/squid.conf



squid -k reconfigure
squid -k check

rc-service squid restart

/bin/bash



