## Use this script to generate self-signed rootCA and SSL certificates


**Features**
* To create self-signed rootCA certificate
* To create rootCA signed certificates for your devices
* SAN and wildcard certificates 

**Usage**
* Copy the input-example.com.txt to your-domain.com and edit the variables
* Run ./gen-rootca-ssl.sh your-domain.com


**To install new rootCA to target OS**

**Option 1: Via Ansible
* Create your-intentory file
* Copy your un-encrypted root CA files to CA folder
* Run the following:

```

ansible-playbook -i your-inventory -l your-host-group ansible-update-trusted-ca.yml

```

**Option 2: Copy manually**

* [ For Debian and Ubuntu OS ]
* scp the root CA file to your target machines 
  * Debian6:/usr/local/share/ca-certificates
  * Debian8:/etc/pki/ca-trust/source/anchors    
* As root, Run update-ca-certificates





