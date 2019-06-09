#### Setup Elasticsearch + Logstash + Kibana using docker compose

Quick way to create ELK ( ElasticSearch + Logstash + Kibana ) using docker.

**Instruction:**

Create a folder your EKL's persistant storage
```
cd ~/
mkdir -p ELK_HOME/CONFIG
cd ELK_HOME
```

**Start up ELK container**
Copy docker-compose.yml file to ELK_HOME folder and kick off the following comamnd:
```
docker-compose up
```

**Configure persistent storage**
```
mkdir -p DATA/ELASTICSEARCH
mkdir -p DATA/LOGSTASH
mkdir -p DATA/KIBANA

docker cp elasticsearch:??/ DATA/ELASTICSEARCH/

docker cp logstash:??/ DATA/LOGSTASH/

docker cp kibana:??/ DATA/KIBANA/

```

**Modify ELK configurations**

```
```
**Delete ELK containers and start up new container with volume mounting**

```

```

