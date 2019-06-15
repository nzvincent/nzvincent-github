#!/bin/sh

#@Author: nzvincent@gmail.com / Vincent Pang
# This script uses inotifywatch to monitor files status and trigger commands.
# To install .eg apt-get install -y inotify-tools
# Download this code to your git clone project directory, do not rename this script.

# Modify below here.
DIR=`pwd`
CMD_PREFIX="ansible-playbook -i hosts.txt -l linux-debian "
GIT_BRANCH=master
GIT_MSG="Ansible successfully built."

if [ ! $@ ]; then
  echo "Error input, Example: $0 playbook-file.yml"
  exit 127
fi

while inotifywait -r --exclude .git -e modify -e create ${DIR}; do
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
