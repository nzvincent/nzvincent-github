#### An Ansible script to install Kubernetes cluster to Centos 7

This project installs Kubernetes cluster master and worker nodes to Centos 7.

##### Requirements:
* At least 1 Centos7 minimum install VM with 2GB RAM, 20GB storage.
* At least 2 Centos7 minimum install VM with 2GB RAMm 20GB storage.
* A NFS file sharing (optional )

##### Architecture overview:

```
                / - Worker node 1 -\
Master node  <=                     => NFS persistent shared storage 
                \-  Worker node 2 -/

```

