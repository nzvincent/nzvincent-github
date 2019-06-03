#### An Ansible script to install Kubernetes cluster to Centos 7

This project installs Kubernetes cluster master and worker nodes and NFS to Centos 7.

##### Requirements:
* At least 1 Centos7 minimum installed VM with 2GB RAM, 20GB storage for Kubernetes master node
* At least 2 Centos7 minimum installed VM with 2GB RAM, 20GB storage for Kubernetes worker nodes.
* A NFS file sharing server to be shared by worker nodes (optional) for NFS persistent storage share.

##### Architecture overview:

```
                           / - Worker node 1 -\
Kubernetes master node  <=                      => NFS persistent shared storage 
                           \-  Worker node 2 -/

```
##### Installation instruction:
The installation includes three parts.
* An automated master and worker nodes intallation using Ansible.
* Linux command line to setup one-off Kubernetes master and worker nodes.
* Deploy 3 replicated NginX web servers using Kubernetes deployment file.

**Provisioning your VM**
First, assuming you've already configured 4 Centos 7 VM with minimun installation for:
* 1 x Kubernetes master node
* 2 x Kubernetes workder nodes
* 1 x NFS server node

**Download Ansible shared projects**
```
git clone https://github.com/nzvincent/shared-projects.git
cd ansible-install-kubernetes-cluster-centos7
```

**Modify inventories and group variables**

Edit the following inventories using your favorite editor, replacing the IPs with your VM IPs.
```
vi inventories/kuberhosts

vi inventories/group_vars/kuber/vars
```

**Install Kubernete docker base system**
```
ansible-playbook -i inventories/kuberhosts -l kuber-master playbook-install-base-system.yml -e reboot=1 -e disable_security=1
```

**Install Kubernete master nodes**
```
ansible-playbook -i inventories/kuberhosts -l kuber-master playbook-install-kubernetes.yml -e reboot=1
```

**Install NFS server to nfs node**
```
ansible-playbook -i inventories/kuberhosts -l kuber-nfs-server playbook-install-nfs-server.yml -e reboot=1
```

**Install NFS client to Kubernetes worker nodes**
```
ansible-playbook -i inventories/kuberhosts -l kuber-worker playbook-install-nfs-client.yml -e reboot=1
```



