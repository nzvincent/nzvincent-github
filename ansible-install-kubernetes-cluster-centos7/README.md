#### An Ansible script to install Kubernetes cluster to Centos 7

This project installs Kubernetes cluster master and worker nodes to Centos 7.

##### Requirements:
* At least 1 Centos7 minimum installed VM with 2GB RAM, 20GB storage.
* At least 2 Centos7 minimum installed VM with 2GB RAM, 20GB storage.
* A NFS file sharing server to be shared by worker nodes (optional)

##### Architecture overview:

```
                / - Worker node 1 -\
Master node  <=                     => NFS persistent shared storage 
                \-  Worker node 2 -/

```
##### Installation instruction:
This instruction includes three parts.
* An automated master and worker nodes intallation using Ansible.
* Linux command line to setup one-off Kubernetes master and worker nodes.
* Deploy 3 replicated NginX web servers using Kubernetes deployment file.

**Install Kubernete docker base system*
```
ansible-playbook -i inventories/kuberhosts -l kuber-master playbook-install-base-system.yml -e reboot=1
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



