#!/bin/bash

wget https://raw.githubusercontent.com/nzvincent/nzvincent-github/master/python/siteDoAutomation/Dockerfile -O Dockerfile
wget https://raw.githubusercontent.com/nzvincent/nzvincent-github/master/python/siteDoAutomation/requirements.txt -O requirements.txt
wget https://raw.githubusercontent.com/nzvincent/nzvincent-github/master/python/siteDoAutomation/siteDo.py -O siteDo.py
wget https://raw.githubusercontent.com/nzvincent/nzvincent-github/master/python/siteDoAutomation/kickstart.py -O kickstart.py

docker build -t "sitedo" .

docker run -it -v`pwd`:/myfile --name sitedo -h sitedo -w /myfile sitedo /bin/bash
