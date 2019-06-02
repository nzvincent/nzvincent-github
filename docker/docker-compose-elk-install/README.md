#### Setup Elasticsearch + Logstash + Kibana using docker compose

Quick way to create ELK ( ElasticSearch + Logstash + Kibana ) using docker.

*Instructions:*
Create a folder your EKL's persistant storage
```
cd ~/
mkdir -p ELK_HOME/CONFIG
cd ELK_HOME
```


Copy docker-compose file to ELK_HOME folder and run:
```
docker-compose up
```


