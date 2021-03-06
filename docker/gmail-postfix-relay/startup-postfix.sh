#!/bin/bash -x

set -e 

# Stop postfix if is running: exit 0
#[ postfix status  ] && postfix stop

if [ -f /etc/postfix/sasl_passwd ]; then
  postmap /etc/postfix/sasl_passwd
  # rm -f /etc/postfix/sasl_passwd
fi

# Enable log
postconf maillog_file=/var/log/postfix.log 

postfix start


