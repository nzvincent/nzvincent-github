#!/bin/sh

#@Author: nzvincent@gmail.com / Vincent Pang
# This script uses inotifywatch to monitor files status and trigger commands.
# I designed this for Ansible playbook but you can use this on other development purposes.
# To install .eg apt-get install -y inotify-tools
# Download this code to your git clone project directory, do not rename this script.
# Usage:
#   - Copy this script to your cloned git root directory. 
#   - Modify the variables
#   - Change file permission to - chmod 0744 inotify.sh
#   - on your git project root directory, Run ./inotify.sh, 
# Notes: this script will utilise your terminal during inotify watch, so you may need to start up another terminal.


# Modify variables below here.

MONDIR=`pwd`
# -r is recursive, you can exclude .git .svn -e is what event to be monitored
INOTIFY_OPT="-r --exclude .git -e modify -e create"  
# Build command prefix to be triggered when change made
CMD_PREFIX="ansible-playbook -i hosts.txt -l linux-debian "
# Git commit options on build success. 
GIT_BRANCH=master
GIT_MSG="Ansible successfully built."


# CMD_PREFIX $@, command prefix [ arguments ] eg. ansible-playbook -i hosts.txt -l linux-debian [ playbook.yml ]
if [ ! $@ ]; then
  echo "Input error!!!, example: $0 playbook-file.yml"
  exit 127
fi

while inotifywait ${INOTIFY_OPT} ${MONDIR}; do
   ${CMD_PREFIX} $@
   EXIT=$?
   if [ $EXIT -eq 0 ]; then
     echo "Build successful and kick off git commit"
     git add .
     git reset infotify.sh
     git status
     git commit -m "${GIT_MSG}"
     git push origin ${GIT_BRANCH}
   else
     echo "Build failed, No push to Git"
   fi
done
