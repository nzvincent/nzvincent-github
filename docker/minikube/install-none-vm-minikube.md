## Install minikube test lab

This install minikube on single VM, all kubenetes components will be installed on Docker containers.

## Install docker
* Debian https://docs.docker.com/install/linux/docker-ce/debian/
* Centos https://docs.docker.com/install/linux/docker-ce/centos/
* Fedora https://docs.docker.com/install/linux/docker-ce/fedora/
* SLEX https://docs.docker.com/install/linux/docker-ee/suse/

### Install minikube
* https://kubernetes.io/docs/tasks/tools/install-minikube/

## MiniKube without VM ( docker based )
* https://medium.com/@nieldw/running-minikube-with-vm-driver-none-47de91eab84c
* ```minikube start --vm-driver=none --apiserver-ips 127.0.0.1 --apiserver-name localhost```

## install Kubectl release
* https://github.com/kubernetes/kubernetes/releases

## Install miniKube 
* https://kubernetes.io/docs/tasks/tools/install-minikube/

## Deploy persistent volume
* This is working example.
* need to build docker image. eg. docker build -t research:v2 .
* need to deploy persistent PVC using kubectl apply -f deploy-persistent-vol.yaml
* Deploy application. kubectl apply -f deploy-research.yaml ( note, this file have tiny leading tab/space issue ) 
* https://martincarstenbach.wordpress.com/2019/06/07/learning-kubernetes-persistent-storage-with-minikube/ 
