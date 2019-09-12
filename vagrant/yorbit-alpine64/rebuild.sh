#!/bin/bash

echo "Stop VM: $(vagrant halt)"

echo "Destroy VM: $(vagrant destroy)"

echo "Clean up vagrant files : $(vagrant global-status --prune)"

echo "Remove .vagrant: $(rm -rf .vagrant)"

echo "Validate Vagrantfile: $(vagrant validate)"

echo " "
echo "To start vagrant with stdout and stderr output"
echo "Usage: vagrant up --debug 2>&1 | tee vagrant.log"
