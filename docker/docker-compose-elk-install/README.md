#### Setup Elasticsearch + Logstash + Kibana using docker compose

Quick way to create ELK ( ElasticSearch + Logstash + Kibana ) using docker.

**Instruction:**

Create a folder your EKL's persistant storage
```
cd ~/
mkdir -p ELK_HOME
cd ELK_HOME

mkdir -p DATA/ELASTICSEARCH
mkdir -p DATA/LOGSTASH
mkdir -p DATA/KIBANA

mkdir -p CONFIG/ELASTICSEARCH
mkdir -p CONFIG/LOGSTASH
mkdir -p CONFIG/KIBANA
```

**Start up ELK container**

Copy docker-compose.yml file to ELK_HOME folder and kick off the following comamnd:
```
docker-compose up
```

**Configure persistent storages**

```
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

