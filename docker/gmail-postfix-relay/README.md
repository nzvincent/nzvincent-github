# Postfix Gmail Relay 

*Before setting up, you need to login to GMAIL to setup Application password.*
https://support.plesk.com/hc/en-us/articles/115004947113-How-to-set-up-Postfix-to-send-emails-using-Gmail-Relay-with-authentication-

## Building docker image
```
docker build -t "alpine-postfix:homebrew" .
```

## Start up docker container
```
docker run -it \
  -h postfix --name postfix \
  --restart always \
  -v /etc/localtime:/etc/localtime:ro \
  -v /etc/timezone:/etc/timezone:ro \
  -p 25:25 \
  -e RELAYHOST smtp.gmail.com \
  -e RELAYHOST_PORT 587 \
  -e RELAYHOST_USER your-gmail-id \
  -e RELAYHOST_PASSWORD your-gmail-app-password \
  -e MYHOSTNAME my-domain.com \
  -e INET_INTERFACE all \
  -e MYNETWORK_STYLE host \
  -e MYNETWORKS "172.15.0.0/24 192.168.1.0/24" \
  -e MYHOSTNAME smtp-your-domain.com \
  -e MYDOMAIN your-domain.com \
  alpine-postfix:homebrew \ 

```
