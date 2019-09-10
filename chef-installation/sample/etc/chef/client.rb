log_level               :trace
log_location            STDOUT
ssl_verify_mode         :verify_none
verify_api_cert         false
chef_server_url         "https://chef-server/organizations/yorbit"
validation_client_name  "yorbit-validator"
validation_key          "/etc/chef/yorbit-validator.pem"
node_name               "kube-master"
