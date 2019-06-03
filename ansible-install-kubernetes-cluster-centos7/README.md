#### An Ansible script to install Kubernetes cluster on Centos 7

This project installs Kubernetes cluster master and worker nodes and NFS server to Centos 7.

#### Requirements:
* At least 1 Centos7 minimum installed VM with 2GB RAM, 20GB storage for Kubernetes master node
* At least 2 Centos7 minimum installed VM with 2GB RAM, 20GB storage for Kubernetes worker nodes.
* A NFS file sharing server to be shared by worker nodes (optional) for NFS persistent storage share.

#### Architecture overview:

```
                           / - Worker node 1 -\
Kubernetes master node  <=                      => NFS persistent shared storage 
                           \-  Worker node 2 -/

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

Your virtual machines can be Vmware, KVM or Virtualbox. I created and tested this project on KVM.

**Step 2: Download Ansible shared projects**
```
git clone https://github.com/nzvincent/shared-projects.git
cd ansible-install-kubernetes-cluster-centos7
```

**Step 3: Modify inventories and group variables**

Edit the following inventories using your favorite editor, replacing the IPs with your VM IPs.
```
vi inventories/kuberhosts

vi inventories/group_vars/kuber/vars
```

**Step 4: Kick off Ansible playbooks**

*Install Kubernete docker base system*
```
ansible-playbook -i inventories/kuberhosts -l kuber-master playbook-install-base-system.yml -e reboot=1 -e disable_security=1
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



