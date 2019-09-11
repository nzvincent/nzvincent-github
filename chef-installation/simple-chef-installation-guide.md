# Installing Chef Server / ChefDK ( Chef Workstation ) / Chef Client

This is my first attempt to install Chef and there are a lot more to learn. This instruction is based on Chef Doc and some Youtubers videos but I condensed it into one page document. The lab scenario is designed for testing purpose only.

> **Important Notes**
- Chef unable to run on Docker, use VM instead.
- All Chef servers and nodes/clients clocks to be in-sync. Make sure you install NTP on all your hosts and keep the time in-sync.
- My Lab environments setup are:
   - 1 x Chef Infra Server Standalone ( Ubuntu 18.04.3 LTS )
   - 1 x ChefDK Chef Workstation ( Debian 9 )
   - 1 x Chef client/node ( Centos 7 )
   

**Preparation** 

If you do not have a DNS server running on your network, you need to hardcode the DNS to all your
hosts. modify the IP addresses and append the followowing lines to your 
- Linux : /etc/hosts files. 
- Windows: C:\Windows\System32\drivers\etc\hosts ( You must be Administrator to edit this file )
- Example: ( recommended FQDN but hostname should be fine )

```
chef-server       192.168.1.100
chef-workstation  192.168.1.101
chef-client       192.168.1.102
```
- Make sure your Chef server hostname is **chef-server** by editting /etc/hostname, otherwise your SSL certification will have trouble to be trusted by clients later.
- For chef workstations and client machines, ensure the main non root user has the sudo root privillege ( recommended using NOPASSWD in the visudo )
- nano, wget and curl are installed

## To Install Chef Server ( Ubuntu 18.04.3 LTS ) 
- My Chef Server Lab environments:
  - Linux localhost 4.15.0-60-generic #67-Ubuntu SMP Thu Aug 22 16:55:30 UTC 2019 x86_64 x86_64 x86_64 GNU/Linux
  - PRETTY_NAME="Ubuntu 18.04.3 LTS"
- 2 packages to be installed to Chef server are **chef-server** and **chef-manage**
- Instruction: https://docs.chef.io/install_server.html#standalone
- Download **Chef infra Server** https://downloads.chef.io/
  - Select **Chef Infra Server** and click download ( You may be asked to enter your personal information )
  - my version of md5sum: ```700bb3d8e240093a2377e23b845636d1``` chef-server-core_12.18.14-1_amd64.deb
- As a root user on the Chef Server
- Run install: ``` dpkg -i chef-server-core_12.18.14-1_amd64.deb ```
- After instalation completed, initialise configuration by running: ```chef-server-ctl reconfigure```
  - When finished, you should see ```Chef Client finished, 494/1101 resources updated in 05 minutes 59 seconds
Chef Server Reconfigured!```
- Verify configuration by running: ```chef-server-ctl status```, you will see: 


```
run: bookshelf: (pid 1530) 125s; run: log: (pid 1542) 124s
run: nginx: (pid 1353) 129s; run: log: (pid 1870) 119s
run: oc_bifrost: (pid 1268) 131s; run: log: (pid 1332) 130s
run: oc_id: (pid 1342) 130s; run: log: (pid 1348) 129s
run: opscode-erchef: (pid 1730) 122s; run: log: (pid 1664) 123s
run: opscode-expander: (pid 1424) 126s; run: log: (pid 1524) 125s
run: opscode-solr4: (pid 1387) 127s; run: log: (pid 1404) 127s
run: postgresql: (pid 1260) 131s; run: log: (pid 1264) 131s
run: rabbitmq: (pid 2756) 96s; run: log: (pid 1885) 118s
run: redis_lb: (pid 27255) 328s; run: log: (pid 1863) 119s

```

- Next, you need to install **Chef-Manage** to be able to use the Chef Server web interface. I tried the chef-server-ctl by following the website instruction to install but failed, so It's better to install it from the binary.
- Download **Chef Manage** binary from: https://downloads.chef.io/
  - my version of md5sum: ```f1cda551a33c33aebdd8b93e6cfd57b9```  chef-manage_2.5.16-1_amd64.deb
- To install as root user, run: ```dpkg -i chef-manage_2.5.16-1_amd64.deb```
- After installation completed, run:
  - ```chef-manage-ctl reconfigure```
  - ```chef-server-ctl reconfigure``` ( recommened to run this but I didn't )
 - To verify, Run: ```chef-manage-ctl status```, you will see:
 
```
run: redis: (pid 1926) 41350s; run: log: (pid 1932) 41349s
run: web: (pid 1937) 41349s; run: log: (pid 1943) 41348s
run: worker: (pid 1912) 41351s; run: log: (pid 1947) 41348s

```

- **Final step**, you need to create admin user and orginasation and store the private keys, so that it can be used by ChefDK/Chef workstations and Chef Clients to join the service.
- Create folder on your /root directory. ```mkdir -p /root/chef-keys/```
- To add the first admin user, run:

```
chef-server-ctl user-create admin FIRST_NAME LAST_NAME admin@example.com 'REPLACE_YOUR_PASSWORD' \
--filename /root/chef-keys/admin.pem
```
- To add organisation, eg. ABC run: 

```
chef-server-ctl org-create abc 'ABC INC' --association_user admin \
--filename /root/chef-keys/abc-validator.pem
 ```
- Now you can access your Chef Server web interface using your admin password that you've created.
  - https://chef-server


## Install ChefDK on Chef workstation 
- When install chefDK, it will also installing chef-client, embeded Ruby for your chef workstation.
- To download, run ```wget https://packages.chef.io/files/stable/chefdk/3.2.30/ubuntu/18.04/chefdk_3.2.30-1_amd64.deb```, can also be downloaded from https://downloads.chef.io/
- As a root user, run ```dpkg -i chefdk_3.2.30-1_amd64.deb```
- After installation, should see:

```
Selecting previously unselected package chefdk.
(Reading database ... 160441 files and directories currently installed.)
Preparing to unpack chefdk_3.2.30-1_amd64.deb ...
Unpacking chefdk (3.2.30-1) ...
Setting up chefdk (3.2.30-1) ...
Thank you for installing Chef Development Kit!
```
- After installed chefDK, you can switch to normal non root user.
- As a normal user, export ruby path ```export PATH="/opt/chefdk/embedded/bin:$PATH"```.
- or, you could add that to your bashrc or bash_profile so that path will be added when you login. ( please Googling it )
- Verify by running: ```chef-client -v```, it should output something like ```Chef: 14.4.56```
- **Next**, you need to configure your machine to join the chef-server.
- Go to https://chef-server, click Adminstration, then click on your organisation. eg. abc, on the left navigation menu, click on the **Starter Kit** to download the Starter Kit zip file.
- Transfer the Starter Kit zip file to your Linux Chef workstation user home directory and unzip it.
- This will extract folders and files to */home/YOUR_USER/chef-repo* directory.
- Create a symbolic link of your .chef directory to your ~/,  Run ```cd ~/``` , Run ```ln -s chef-repo/.chef .```
- Go to ~/chef-repo directory, and run ```knife client list``` and ```knife ssl check```, you may see some error message, it's because you do not have the trusted SSL certificate on your workstation PC.
- Run ```knife ssl fetch``` , this will download trusted SSL certificate to your ~/chef-repo/.chef/trusted_certs/ folder.
- Run ```knife client list``` and you will see something like *abc-validator*
- **NEXT**, Register the node ( client ) by running ```knife bootstrap chef-workstation -N ws``` on your workstaiton. **chef-workstation** this the node hostname and *ws* is client reference ( I guess...) You will be prompted to enter root password for your target ( client ) machine, please ensure your sshd_config on your target machine is *PermitRootLogin yes* and sshd service is reloaded.

```
user@chef-workstation:~/chef-repo/cookbooks/firstjob/recipes$ 
knife bootstrap chef-workstation -N ws
Node ws exists, overwrite it? (Y/N) Y
Client ws exists, overwrite it? (Y/N) Y
Creating new client for ws
Creating new node for ws
Connecting to chef-workstation
root@chef-workstation's password:
chef-workstation -----> Existing Chef installation detected
chef-workstation Starting the first Chef Client run...
chef-workstation Starting Chef Client, version 14.4.56
chef-workstation resolving cookbooks for run list: []
chef-workstation Synchronizing Cookbooks:
chef-workstation Installing Cookbook Gems:
chef-workstation Compiling Cookbooks...
chef-workstation [2019-09-10T15:00:25+12:00] WARN: Node ws has an empty run list.
chef-workstation Converging 0 resources
chef-workstation
chef-workstation Running handlers:
chef-workstation Running handlers complete
chef-workstation Chef Client finished, 0/0 resources updated in 03 seconds
user@chef-workstation:~/chef-repo/cookbooks/firstjob/recipes$
user@chef-workstation:~/chef-repo/cookbooks/firstjob/recipes$
```
- Now you can verify the client nodes via ```knife client list```, your **ws** node will be listed on the command output.
- **DONE**, next you can create your first cookbook using **chef** command.

## Create your first cookbook 
- On the workstation machine as user, go to ~/chef-repo and RUN: ```chef generate cookbook firstjob``` to generate your first job. This will create a *firstjob* folder with bunch of files and sub directories.
- Move the *firstjob* directory to *cookbooks* folder by running ```mv firstjob cookbooks```
- Go to ```cd cookbooks/firstjob/``` and run ```ls``` and you will see something like ```Berksfile  CHANGELOG.md  chefignore  LICENSE  metadata.rb  README.md  recipes  spec  test```
- Example, if you want to install package/app to the target machines.
- Edit recipes/default.rb file. file should look something like this 

```
#
# Cookbook:: firstjob
# Recipe:: default
#
# Copyright:: 2019, The Authors, All Rights Reserved.

package 'nmap' do
  action :install
end

```
- Make sure **:install** without space, this may be ruby syntax. not sure why.
- Next, upload all cookbook to server by running ```knife cookbook upload -a``` and you shall see something like:

```
Uploading firstjob     [0.1.0]
Uploading starter      [1.0.0]
Uploaded all cookbooks.
```
- Next, you need to add the cookbook to the client list.
- Before run this, you may need to export your EDITOR by running ```export EDITOR=/bin/nano``` depending on which editor you are installed on your chef-workstation.
- An default EDITOR will open up json file an you can add the cookbook recipe and client node to the run list.
- Run: ```knife node edit ws``` and add your recipe to the run_list **"recipe[firtjob]"**

```
....

"run_list": [
	"recipe[firtjob]"
	]
```
- You also need to ensure that your /etc/chef/client.pem is accessible by the current user. ( If not, change the chmod to 740 )
- **Finally**, Run ```chef-client```, to revealing the moment of truth.
- If is successful, you will see something like the following:

```
user@chef-workstation:/etc/chef$ chef-client
Starting Chef Client, version 14.4.56
resolving cookbooks for run list: ["firstjob"]
Synchronizing Cookbooks:
  - firstjob (0.1.0)
Installing Cookbook Gems:
Compiling Cookbooks...
Converging 1 resources
Recipe: firstjob::default
  * apt_package[nmap] action install (up to date)

Running handlers:
Running handlers complete
Chef Client finished, 0/1 resources updated in 02 seconds

```


## Installing Chef client and register node to the Chef server
- ssh to your target node
- mkdir /etc/chef/
- create 3 files

```
/etc/chef/
  |- abc-validator.pem
  |- first-boot.json
  \_ clinet.rb 
 ``` 
- abc-validator.pem ( You can use the web UI Admin/Organisation to reset the validation key )
- firt-boot.json  ( recommended to use web ui to create a default base role and leave it empty )
 
```
 {"run_list":[
    "role[base]"
 ]}

```
- client.rb file ( node_name is the name that you want to name your node, it's not FQDN can be anyname )

```
log_level               :trace
log_location            STDOUT
ssl_verify_mode         :verify_none
verify_api_cert         false
chef_server_url         "https://chef-server/organizations/yorbit"
validation_client_name  "abc-validator"
validation_key          "/etc/chef/abc-validator.pem"
node_name               "chef-node1"

 ```

- **NEXT**, run the following ```curl -L https://omnitruck.chef.io/install.sh | sudo bash``` on the client node to install packages.
- Next, **Register your client node to chef server** by running ```chef-client -j /etc/chef/first-boot.json```
- Once it has done, your /etc/chef/ will create a client.pem authentication file. You can remove abc-validator.pem as it's no longer needed.
- Once it's successully registered, you will see the new node registered on your Chef server web UI.
- **Important notes**: Make sure you keep the clock in-sync, you can turn on log_level :trace on your client.rb to trace error if you encountering problem when running the register.
 
 
## Troubleshooting

```
# Export PATH and EDITOR to your ~/.bashrc or ~/.bash_profiles
PATH="/opt/chefdk/embedded/bin:$PATH"
export EDITOR=/bin/nano
```

## Cheatsheet

**For ChefDK**

```

# Generate new cookbook
chef generate cookbook myfirstjob

# Modify myfirstjob cookbook, define what to be executed
nano ~/chef-repo/cookbooks/myfirstjob/recipes/default.rb

# Edit run list , what recipe to be run on target node
knife node edit NODE_NAME

# Upload all cookbook to Chef server
knife cookbook upload -a

# Exacute cookbook and push change to target machine
chef-client

# Using bootstrap to push changes to target machine
knife bootstrap TARGET_MACHINE_HOST --ssh-user TARGET_MACHINE_USER --sudo --node-name CHEF_SERVER_REG_NODE_NAME --run-list 'recipe[firstjob]'

# other option: --identify-file ~/.chef/login.pem 


```

**For Client node**
```

# Register node to Chef Server
chef-client -j /etc/chef/first-boot.json

# Check registered node on Chef server
knife client list


```

**Other commands**

```
knife client show NODE_NAME


```



