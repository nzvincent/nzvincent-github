# Install Docker and Kubernates to Alpine Linux

Docker 
http://web.ist.utl.pt/joao.leao.guerreiro/post/alpinedocker/

Kubernates
https://dev.to/xphoniex/how-to-create-a-kubernetes-cluster-on-alpine-linux-kcg


apk add kubeadm kubectl kubelet

swapoff -a
rc-update add docker default
rc-update add kubelet default

kubeadm init --apiserver-advertise-address=192.168.1.19 --kubernetes-version=1.20.0



