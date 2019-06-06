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
ansible-playbook -i inventories/kuberhosts -l kuber-master playbook-install-base-system.yml \
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



