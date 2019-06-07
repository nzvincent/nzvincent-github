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
                                                 / - Worker node 1 -\
Kubectl(any OS ) --> Kubernetes master node  <=                      => NFS persistent shared storage / Database 
(Manage Kubernetes)                              \-  Worker node 2 -/

```
## Installation:
The installation includes three parts.
* An automated master, worker and NFS nodes intallation using Ansible.
* Linux command line to setup one-off Kubernetes master and worker nodes pairing.
* Deploy 3 replicated Nginx loadbalance proxy using Kubernetes deployment and Docker.

**Step 1: Provisioning your Virtual Machines** 

First, assuming you've already configured 4 Centos 7 VMs with minimun installation for:
* 1 x Kubernetes master node
* 2 x Kubernetes worker nodes
* 1 x NFS server node

Your physical / virtual machines can be Vmware, KVM or Virtualbox. this project is tested on KVM.

**Step 2: Download Ansible scripts from my Github projects (Part 1)** 
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

**Step 5: Setup Kubernetes master and workers pairing (Part 2)**

*Initialize and setup kubernetes master node*
Once completed, you should see *Your Kubernetes master has initialized successfully!*
```
[root@kuber-master ~]# kubeadm init --apiserver-advertise-address=10.0.15.10 --pod-network-cidr=10.244.0.0/16
```

*Copy the **kubeadm join.....** from the kubeadm init output to your text editor, the command will then be used on worker nodes to register new nodes to Kubernetes cluster*

*Setup user's kubectl configuration*
```
[root@kuber-master ~]#
mkdir -p $HOME/.kube
cp -i /etc/kubernetes/admin.conf $HOME/.kuber/config
chown $(id -u):$(id -g) $HOME/.kuber/config
```

*Deploy flannel network to Kubernetes cluster*
```
[root@kuber-master ~]#
kubectl apply -f https://raw.githubusercontent.com/coreos/flannel/master/Documentation/kube-flannel.yml
```

*Verify nodes and pods*
```
[root@kuber-master ~]#
kubectl get nodes
kubectl get pods --all-namespaces
```

*Go to worker nodes to join workers to Kubernetes master* 
Example:
```
[root@kuber-master ~]#
kubeadm join 10.0.15.10:6443 --token vzau5v.vjiqyxq26lzsf28e --discovery-token-ca-cert-hash sha256:e6d046ba34ee03e7d55e1f5ac6d2de09fd6d7e6959d16782ef0778794b94c61e

```



