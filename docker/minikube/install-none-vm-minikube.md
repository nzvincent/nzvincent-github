## Install minikube test lab

## Install docker

### Install minikube
* https://kubernetes.io/docs/tasks/tools/install-minikube/

## MiniKube without VM ( docker based )
* https://medium.com/@nieldw/running-minikube-with-vm-driver-none-47de91eab84c

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







