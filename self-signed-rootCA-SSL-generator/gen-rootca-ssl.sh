#/bin/bash -x

# This script generates CA and Device CERT
# @Author: nzvincent@gmail.com
# Usage:
# ./gen-rootca-ssl.sh
# ./gen-rootca-ssl.sh inputfile

BACKUP=backup-`date '+%Y%m%d%H%M%S'`
mkdir -p ${BACKUP}
[ -d ${BACKUP} ] && cp -pv *.csr *.key *.crt *.cnf *.srl serial *.txt ${BACKUP} 

# Re-generate rootCA key and certificate
REGEN_CA_KEY=NO
REGEN_CA_CRT=NO

CA_DNS=ca.example.com
HOST_DNS=www.example.com
CA_KEY_PASS="topsecret"
HOST_KEY_PASS="lastsecret"

CITY=Wellington
COUNTRY=NZ
EMAIL=ca@example.com
ORG="Example Org"
UNIT="Example Unit"

# Subject Alternative Name ( SAN )
ALT_DNS="
DNS.1 = *.example.com
DNS.2 = www.example.com
DNS.3 = www1.example.com"

# Private key encryption cipher
CA_KEY_CIPHER="aes256" 
HOST_KEY_CIPHER="aes256" 

# Secure Hashing Algorithm
CA_SHA=sha256
HOST_SHA=sha256

# Certificate expiry
CA_EXPIRE_DAY=3560
HOST_EXPIRE_DAY=730

INPUT=$1
[ -f ${INPUT} ] && source $INPUT

CA_KEY=rootCA-${CA_DNS}.key
CA_CRT=rootCA-${CA_DNS}.crt
CA_CFN=rootCA-${CA_DNS}.cfn

HOST_KEY=device-${CA_DNS}.key
HOST_CSR=device-${CA_DNS}.csr
HOST_CRT=device-${CA_DNS}.crt
HOST_CFN=device-${CA_DNS}.cfn

INDEX=index.txt
SERIAL=serial

echo > ${CA_CFN}
cat <<EOT >> ${CA_CFN}

  [ req ]
  prompt                  = no
  distinguished_name      = special_name

  [ special_name ]
  commonName              = ${CA_DNS}
  stateOrProvinceName     = ${CITY}
  countryName             = ${COUNTRY}
  emailAddress            = ${EMAIL}
  organizationName        = ${ORG}
  organizationalUnitName  = ${UNIT}

EOT

echo > ${HOST_CFN}
cat <<EOT >> ${HOST_CFN}

  [ req ]
  prompt                  = no
  distinguished_name      = special_name
  req_extensions          = req_ext

  [ special_name ]
  commonName              = ${HOST_DNS}
  stateOrProvinceName     = ${CITY}
  countryName             = ${COUNTRY}
  emailAddress            = ${EMAIL}
  organizationName        = ${ORG}
  organizationalUnitName  = ${UNIT}

  [ req_ext ]
  subjectAltName = @alt_names

  [alt_names]
  ${ALT_DNS}

EOT


h1 (){
  echo "#################################################"
  echo "# $@ "
  echo "#################################################"
  echo " "
  sleep 1
}


# update time server

############################################
# rootCA signer KEY / CERT
############################################
touch ${INDEX}
echo "1234" > ${SERIAL}

# Set generate rootCA key and cert to Yes if not available 
[ ! -f "${CA_KEY}" ] && REGEN_CA_KEY="YES"
[ ! -f "${CA_CRT}" ] && REGEN_CA_CRT="YES"

if [ "${REGEN_CA_KEY}" == "YES" ]; then

  h1 "Create rootCA key"
  openssl genrsa -${CA_KEY_CIPHER} \
  -passout pass:${CA_KEY_PASS} \
  -out ${CA_KEY} 2048 \

else
  h1 "SKIP: rootCA key"
fi

if [ "${REGEN_CA_CRT}" == "YES" ]; then

  h1 "Generate rootCA cert"
  openssl req -new -x509 -nodes \
  -${CA_SHA} \
  -days ${CA_EXPIRE_DAY} \
  -key ${CA_KEY}\
  -passin pass:${CA_KEY_PASS} \
  --config ${CA_CFN} \
  -out ${CA_CRT} \

else
  h1 "SKIP: rootCA cert"
fi


h1  "Verify rootCA cert"
openssl x509 -noout -text \
  -in ${CA_CRT}

############################################
# Device's key and CSR
############################################
h1 "Create device's key"
openssl genrsa -${HOST_KEY_CIPHER} \
  -passout pass:${HOST_KEY_PASS} \
  -out ${HOST_KEY} 2048

h1 "Generate device's csr"
openssl req -new \
  -key ${HOST_KEY} \
  -passin pass:${HOST_KEY_PASS} \
  -config ${HOST_CFN} \
  -out ${HOST_CSR}
  
h1 "Verify device's csr"
openssl req -noout -text \
  -in ${HOST_CSR}

############################################
# Device's Cert
############################################
h1 "Generate device's cert"
openssl x509 -req -${HOST_SHA} \
  -days ${HOST_EXPIRE_DAY} \
  -in ${HOST_CSR} \
  -CA ${CA_CRT} \
  -CAkey ${CA_KEY} \
  -CAcreateserial \
  -passin pass:${CA_KEY_PASS} \
  -out ${HOST_CRT}

h1 "Verify device's cert"
openssl x509 -noout -text \
  -in ${HOST_CRT}
  
h1 "Secure private keys"
chmod 600 *.key

############################################
# Decrypt private key
# reference: https://www.digicert.com/csr-ssl-installation/ubuntu-server-with-apache2-openssl.htm
############################################
h1 "To decrypt encrypted private key"
openssl rsa -in ${HOST_KEY} -out ${HOST_KEY}.decrypted -passin pass:${CA_KEY_PASS}

# You don't need to decrypt rootCA key in most cases
# openssl rsa -in ${CA_KEY} -out ${CA_KEY}.decrypted -passin pass:${CA_KEY_PASS}

h1 "Secure private keys"
chmod 600 *.key
chmod 600 *.key.decrypted



echo "Copy rootCA cert to your desktop / PC and import the cert to your OS or App trusted keystore"
echo "Keep your private keys and passphrase in a secure place"
echo "Install device's cert and key to your device. eg. Apache"

