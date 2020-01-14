#!/bin/bash -x

# Run this once after docker run

set -e

# [[ if true ]] && this is false || this is true 

# SMTP relay host
[[ -e $RELAYHOST ]] && export POSTFIX_RELAYHOST="smtp.gmail.com" || export POSTFIX_RELAYHOST=$RELAYHOST
[[ -e $RELAYHOST_PORT ]] && export POSTFIX_RELAYHOST_PORT="587" || export POSTFIX_RELAYHOST_PORT=$RELAYHOST_PORT

# SMTP login
[[ -e $RELAYHOST_USER ]] && export POSTFIX_RELAYHOST_USER="dummy-gmail-user" || export POSTFIX_RELAYHOST_USER=$RELAYHOST_USER
[[ -e $RELAYHOST_PASSWORD ]] && export POSTFIX_RELAYHOST_PASSWORD="dummy-gmail-password" || export POSTFIX_RELAYHOST_PASSWORD=$RELAYHOST_PASSWORD 

# POSTFIX configuration
# Network
[[ -e $INET_INTERFACE ]] && export POSTFIX_INET_INTERFACE="all" || export POSTFIX_INET_INTERFACE=$INET_INTERFACE 
[[ -e $MYNETWORK_STYLE ]] && export POSTFIX_MYNETWORK_STYLE="host" || export POSTFIX_MYNETWORK_STYLE=$MYNETWORK_STYLE 
[[ -e $MYNETWORKS ]] && export POSTFIX_MYNETWORKS="all" || export POSTFIX_MYNETWORKS=$MYNETWORKS 
# Hostname
[[ -e $MYMAILHOST ]] && export POSTFIX_MYMAILHOST="your-smtp-domain.com" || export POSTFIX_MYMAILHOST=$MYMAILHOST 
[[ -e $MYDOMAIN ]] && export POSTFIX_MYDOMAIN="your-domain.com" || export POSTFIX_MYDOMAIN=$MYDOMAIN 

# Environment variables substitution 
envsubst < /root/WORKSPACE/postfix-main.cf >> /etc/postfix/main.cf 
envsubst < /root/WORKSPACE/postfix-sasl_passwd >> //etc/postfix/sasl_passwd

# Start up postfix after environment ready
/root/WORKSPACE/startup-postfix.sh

env


# Prevent termination of console
#sleep 1000
sh













