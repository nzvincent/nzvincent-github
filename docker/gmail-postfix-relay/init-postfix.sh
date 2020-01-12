#!/bin/bash

# Run this once after docker run

set -e

# SMTP relay host
[[ -e $RELAYHOST ]] && export POSTFIX_RELAYHOST=$RELAYHOST || export POSTFIX_RELAYHOST="smtp.gmail.com"
[[ -e $RELAYHOST_PORT ]] && export POSTFIX_RELAYHOST_PORT=$RELAYHOST_PORT || export POSTFIX_RELAYHOST_PORT="587"

# SMTP login
[[ -e $RELAYHOST_USER ]] && export POSTFIX_RELAYHOST_USER=$RELAYHOST_USER || export POSTFIX_RELAYHOST_USER="your-gmail-user"
[[ -e $RELAYHOST_PASSWORD ]] && export POSTFIX_RELAYHOST_PASSWORD=$RELAYHOST_PASSWORD || export POSTFIX_RELAYHOST_PASSWORD="12345678"

# POSTFIX configuration
# Network
[[ -e $INET_INTERFACE ]] && export POSTFIX_INET_INTERFACE=$INET_INTERFACE || export POSTFIX_INET_INTERFACE="all"
[[ -e $MYNETWORK_STYLE ]] && export POSTFIX_MYNETWORK_STYLE=$MYNETWORK_STYLE || export POSTFIX_MYNETWORK_STYLE="host"
[[ -e $MYNETWORKS ]] && export POSTFIX_MYNETWORKS=$MYNETWORKS || export POSTFIX_MYNETWORKS="all"
# Hostname
[[ -e $MYHOSTNAME ]] && export POSTFIX_MYHOSTNAME=$MYHOSTNAME|| export POSTFIX_MYHOSTNAME="smtp-your-domain.com"
[[ -e $MYDOMAIN ]] && export POSTFIX_MYDOMAIN=$MYDOMAIN || export POSTFIX_MYDOMAIN="your-domain.com"


# Environment variables substitution 
envsubst < $WORKDIR/postfix-main.cf >> /etc/postfix/main.cf 
envsubst < $WORKDIR/postfix-sasl_passwd >> //etc/postfix/sasl_passwd

# Start up postfix after environment ready
/root/config/startup-postfix.sh

# Prevent termination of console
sh 













