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
#   - Run ./inotify.sh and the script will monitor files status and trigger commands. 

# Modify variables below here.
DIR=`pwd`
INOTIFY_OPT="-r --exclude .git -e modify -e create"
CMD_PREFIX="ansible-playbook -i hosts.txt -l linux-debian "
GIT_BRANCH=master
GIT_MSG="Ansible successfully built."

if [ ! $@ ]; then
  echo "Input error!!!, example: $0 playbook-file.yml"
  exit 127
fi

while inotifywait ${INOTIFY_OPT} ${DIR}; do
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
