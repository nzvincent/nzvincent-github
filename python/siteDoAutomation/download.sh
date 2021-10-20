#!/bin/bash

wget https://raw.githubusercontent.com/nzvincent/nzvincent-github/master/python/siteDoAutomation/Dockerfile -O Dockerfile
wget https://raw.githubusercontent.com/nzvincent/nzvincent-github/master/python/siteDoAutomation/requirements.txt -O requirements.txt
wget https://raw.githubusercontent.com/nzvincent/nzvincent-github/master/python/siteDoAutomation/siteDo.py -O siteDo.py

docker build -t "sitedo:v1" .
