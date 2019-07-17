#!/bin/bash

echo "Give a clean start up for for xfce4 XRDP desktop"

/etc/init.d/xrdp stop

rm /var/run/xrdp/*.pid

/etc/init.d/xrdp stop
/etc/init.d/xrdp start

/bin/bash
