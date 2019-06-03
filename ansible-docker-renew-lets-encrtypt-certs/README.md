#### A snippet to renew Let's encrtyp SSL certificates
Let's encrypt provides CA signed certificates but certificates issued only valide for 3 months.
The objective for this snippet is to make certificates renewal simple.
Recommended to run this from Jenkins or other CI/CD platform. 

#### How this scritp works?
* Trigger Ansible playbook from Jenkins
* Verify your existing expiring certificates.
* Start up ACME docker container to generate Key, Csr and renew certificates from Let's encrtypt site.
* Copy key and certificate to target hosts.
* Verify your web server and reload configuration.
