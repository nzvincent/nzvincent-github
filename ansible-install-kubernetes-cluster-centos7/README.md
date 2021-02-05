## Install Kubernetes cluster master, worker,  NFS on Centos 7 using Ansible playbook

This project installs Kubernetes cluster master and worker nodes and NFS server to Centos 7.
Please note that the implementation is purely for lab purposes, do not use it on production without hardening the security.
I will include environment security uplift next phase.

#### Requirements:
* At least 1 Centos7 minimum installed VM with 2GB RAM, 20GB storage for Kubernetes master node
* At least 2 Centos7 minimum installed VM with 2GB RAM, 20GB storage for Kubernetes worker nodes.
* A NFS file sharing server to be shared by worker nodes for persistent storage share. (optional) 
#### Architecture overview:

```
                                           / - [ Worker node 1 ] -\
[ Any OS]   ==> [ Kubernetes master ]   <==                          ==> [ persistent store ] -  
- kubectl       -kubectl/kubeadm/kubelet   \ - [ Worker node 2 ] -/      - NFS
                                                      |                  - Database
                                                      V
                                              [ other extra services ]
                                     - private docker registry ( local-registry )
                                        
```
## Installation:
The installation includes three parts.
1 An automated master, worker and NFS nodes intallation using Ansible.
2 Linux command line to setup one-off Kubernetes master and worker nodes pairing.
3 Deploy 3 replicated Nginx loadbalance proxy using Kubernetes deployment and Docker.

**Step 1: Provisioning your Virtual Machines** 

First, assuming you've already configured 5 Centos 7 VMs with minimun installation for:
* 1 x Kubernetes master node
* 2 x Kubernetes worker nodes
* 1 x NFS server node
* 1 x other services ( docker private registry )

Your physical / virtual machines can be Vmware, KVM or Virtualbox. this project is tested on KVM.

#### Setup Kubernetes cluster using Ansible script (Part 1)

**Step 2: Download Ansible scripts from my Github projects** 
```
git clone https://github.com/nzvincent/nzvincent-github.git
cd ansible-install-kubernetes-cluster-centos7
```

**Step 3: Modify inventories and group variables**

Edit the following inventories using your favorite editor, replacing the IPs with your VM IPs or hostnames.
```
vi inventories/kuberhosts

vi inventories/group_vars/kuber/vars
```

**Step 4: Kick off Ansible playbooks**

*Install Kubernete docker base system*
```
ansible-playbook -i inventories/kuberhosts -l kuber playbook-install-base-system.yml \
  -e reboot=1 -e disable_security=1
```

*Install Kubernete master nodes*
```
ansible-playbook -i inventories/kuberhosts -l kuber-master playbook-install-kubernetes.yml -e reboot=1
```

*Install NFS server to nfs node*
```
ansible-playbook -i inventories/kuberhosts -l kuber-nfs-server playbook-install-nfs-server.yml -e reboot=1
```

*Install NFS client to Kubernetes worker nodes*
```
ansible-playbook -i inventories/kuberhosts -l kuber-worker playbook-install-nfs-client.yml -e reboot=1
```

*Install Docker private registry*
```
ansible-playbook -i inventories/kuberhosts -l kuber-exta-services playbook-install-docker-registry.yml -e reboot=1
```

*Configure Docker private registry*
```
ansible-playbook -i inventories/kuberhosts -l kuber playbook-config-docker-registry.yml -e reboot=1
```



#### Setup Kubernetes master and workers pairing (Part 2)

**Step 5: Initialize and setup kubernetes master node**

*Run the following command to initialise Kubernetes cluster. Once completed, you should see **Your Kubernetes master has initialized successfully!** *

* **apiserver-advertise-address** is your master node IP address 
* **pod-network-cidr** is private address cidr block that you would like to assign to your cluster pods
```
[root@kuber-master ~]# kubeadm init --apiserver-advertise-address=192.168.1.100 --pod-network-cidr=10.244.0.0/16
```

*Copy the **kubeadm join.....** from the kubeadm init output to your text editor, the command will then be used on worker nodes to register new nodes to Kubernetes cluster*

**Step 6: Setup kubectl user's profile configuration**

*Assuming you are using root user here*
```
[root@kuber-master ~]#
> mkdir -p $HOME/.kube
> cp -i /etc/kubernetes/admin.conf $HOME/.kuber/config
> chown $(id -u):$(id -g) $HOME/.kuber/config
```

**Step 7: Deploy flannel network to Kubernetes cluster**
```
[root@kuber-master ~]#
kubectl apply -f https://raw.githubusercontent.com/coreos/flannel/master/Documentation/kube-flannel.yml
```

*Verify nodes and pods*
```
[root@kuber-master ~]#
> kubectl get nodes
> kubectl get pods --all-namespaces
```

**Step 8: Join workers and register nodes to Kubernetes master** 

Copy the command **kubeadm join.....** what you've just pasted to your editor. 
Repeat the command to all your worker nodes. Below is example:

```
[root@kuber-worker ~]#
kubeadm join 10.0.15.10:6443 --token vzau5v.vjiqyxq26lzsf28e \
  --discovery-token-ca-cert-hash \
  sha256:e6d046ba34ee03e7d55e1f5ac6d2de09fd6d7e6959d16782ef0778794b94c61e
```

*Re-run previous step to verify nodes and pods*

You should see list of master and worker nodes.
```
[root@kuber-master ~]#
> kubectl get nodes
> kubectl get pods --all-namespaces
```


#### Deploy Docker containers to Kubernetes cluster (Part 3)

```
[root@kuber-master ~]#

# Create deployment
> kubectl create deployment nginx --image=nginx

# View deployment
> kubectl describe deployment nginx

# Create service and map tcp port numbers
> kubectl create service nodeport nginx --tcp=80:80

# Verify deployed Pods and Services
> kubectl get pods
> kubectl get svc

```

### Renew SSL
https://github.com/kubernetes/kubeadm/issues/581

```
If you are using a version of kubeadm prior to 1.8, where I understand certificate rotation #206 was put into place (as a beta feature) or your certs already expired, then you will need to manually update your certs (or recreate your cluster which it appears some (not just @kachkaev) end up resorting to).

You will need to SSH into your master node. If you are using kubeadm >= 1.8 skip to 2.

    Update Kubeadm, if needed. I was on 1.7 previously.

$ sudo curl -sSL https://dl.k8s.io/release/v1.8.15/bin/linux/amd64/kubeadm > ./kubeadm.1.8.15
$ chmod a+rx kubeadm.1.8.15
$ sudo mv /usr/bin/kubeadm /usr/bin/kubeadm.1.7
$ sudo mv kubeadm.1.8.15 /usr/bin/kubeadm

    Backup old apiserver, apiserver-kubelet-client, and front-proxy-client certs and keys.

$ sudo mv /etc/kubernetes/pki/apiserver.key /etc/kubernetes/pki/apiserver.key.old
$ sudo mv /etc/kubernetes/pki/apiserver.crt /etc/kubernetes/pki/apiserver.crt.old
$ sudo mv /etc/kubernetes/pki/apiserver-kubelet-client.crt /etc/kubernetes/pki/apiserver-kubelet-client.crt.old
$ sudo mv /etc/kubernetes/pki/apiserver-kubelet-client.key /etc/kubernetes/pki/apiserver-kubelet-client.key.old
$ sudo mv /etc/kubernetes/pki/front-proxy-client.crt /etc/kubernetes/pki/front-proxy-client.crt.old
$ sudo mv /etc/kubernetes/pki/front-proxy-client.key /etc/kubernetes/pki/front-proxy-client.key.old

    Generate new apiserver, apiserver-kubelet-client, and front-proxy-client certs and keys.

$ sudo kubeadm alpha phase certs apiserver --apiserver-advertise-address <IP address of your master server>
$ sudo kubeadm alpha phase certs apiserver-kubelet-client
$ sudo kubeadm alpha phase certs front-proxy-client

    Backup old configuration files

$ sudo mv /etc/kubernetes/admin.conf /etc/kubernetes/admin.conf.old
$ sudo mv /etc/kubernetes/kubelet.conf /etc/kubernetes/kubelet.conf.old
$ sudo mv /etc/kubernetes/controller-manager.conf /etc/kubernetes/controller-manager.conf.old
$ sudo mv /etc/kubernetes/scheduler.conf /etc/kubernetes/scheduler.conf.old

    Generate new configuration files.

There is an important note here. If you are on AWS, you will need to explicitly pass the --node-name parameter in this request. Otherwise you will get an error like: Unable to register node "ip-10-0-8-141.ec2.internal" with API server: nodes "ip-10-0-8-141.ec2.internal" is forbidden: node ip-10-0-8-141 cannot modify node ip-10-0-8-141.ec2.internal in your logs sudo journalctl -u kubelet --all | tail and the Master Node will report that it is Not Ready when you run kubectl get nodes.

Please be certain to replace the values passed in --apiserver-advertise-address and --node-name with the correct values for your environment.

$ sudo kubeadm alpha phase kubeconfig all --apiserver-advertise-address 10.0.8.141 --node-name ip-10-0-8-141.ec2.internal
[kubeconfig] Wrote KubeConfig file to disk: "admin.conf"
[kubeconfig] Wrote KubeConfig file to disk: "kubelet.conf"
[kubeconfig] Wrote KubeConfig file to disk: "controller-manager.conf"
[kubeconfig] Wrote KubeConfig file to disk: "scheduler.conf"

    Ensure that your kubectl is looking in the right place for your config files.

$ mv .kube/config .kube/config.old
$ sudo cp -i /etc/kubernetes/admin.conf $HOME/.kube/config
$ sudo chown $(id -u):$(id -g) $HOME/.kube/config
$ sudo chmod 777 $HOME/.kube/config
$ export KUBECONFIG=.kube/config

    Reboot your master node

$ sudo /sbin/shutdown -r now

    Reconnect to your master node and grab your token, and verify that your Master Node is "Ready". Copy the token to your clipboard. You will need it in the next step.

$ kubectl get nodes
$ kubeadm token list

If you do not have a valid token. You can create one with:

$ kubeadm token create

The token should look something like 6dihyb.d09sbgae8ph2atjw

    SSH into each of the slave nodes and reconnect them to the master

$ sudo curl -sSL https://dl.k8s.io/release/v1.8.15/bin/linux/amd64/kubeadm > ./kubeadm.1.8.15
$ chmod a+rx kubeadm.1.8.15
$ sudo mv /usr/bin/kubeadm /usr/bin/kubeadm.1.7
$ sudo mv kubeadm.1.8.15 /usr/bin/kubeadm
$ sudo kubeadm join --token=<token from step 8>  <ip of master node>:<port used 6443 is the default> --node-name <should be the same one as from step 5>

    Repeat Step 9 for each connecting node. From the master node, you can verify that all slave nodes have connected and are ready with:

$ kubectl get nodes




```




