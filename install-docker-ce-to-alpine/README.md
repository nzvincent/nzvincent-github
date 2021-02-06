# Install Docker and Kubernates to Alpine Linux

Docker 
http://web.ist.utl.pt/joao.leao.guerreiro/post/alpinedocker/

Kubernates
https://dev.to/xphoniex/how-to-create-a-kubernetes-cluster-on-alpine-linux-kcg

```
echo "@testing http://dl-cdn.alpinelinux.org/alpine/edge/testing/" >> /etc/apk/repositories
echo "@community http://dl-cdn.alpinelinux.org/alpine/edge/community/" >> /etc/apk/repositories

apk add docker
apk add kubernetes@testing
apk add docker@community
apk add cni-plugins@community

apk add kubectl@testing
apk add kubeadm@testing
apk add kubelet@testing

service docker start

swapoff -a
rc-update add docker default

workers:
rc-update add kubelet default


kubeadm init --apiserver-advertise-address=192.168.1.19 --kubernetes-version=1.20.0

```


apk add kubeadm kubectl kubelet







