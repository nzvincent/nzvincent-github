## To deploy Jenkins master + Jenkins slave agent

This docker compose scritp deploys:

* Jenkins master
* Jenkins slave
* Jfrog artifactory
* Lightweight GIT ( Gogs )


**Steps**

```
cd deploy-jenkins
```

* Modify .env file
* Modify docker-compose.yml 

**Run docker compose**
Run docker compose to build and start containers

```
docker-compose up
```
