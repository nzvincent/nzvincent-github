# Postfix Gmail Relay 

## Scenario
Use Gmail as mail relay to forward your server email externally to the world.

## How it works?
```
Your-server --> Postfix with Gmail relay --> Internet --> Gmail SMTP --> world.
```

*Before setting up gmail smtp postfix relay, you need to login to GMAIL myAccount to setup **App passwords**.*
 * https://support.plesk.com/hc/en-us/articles/115004947113-How-to-set-up-Postfix-to-send-emails-using-Gmail-Relay-with-authentication
 * My Google Account can be found here: https://myaccount.google.com/security

## Building docker image
```
docker build -t "alpine/postfix:homebrew" .
```

## Start up docker container detached mode
*Notes*
* Replace variables with yours.
* RELAYHOST_PASSWORD is NOT your gmail login password, it has to be generated using Google **App Passwords**. https://myaccount.google.com/security
* MYNETWORKS is network of container, you can startup a docker container in your network and run ```ip addr``` to find out. Otherwise Postfix will deny the hosts in your network relaying the email.
* MYHOSTNAME is your arbitrary STMP host.
* MYDOMAIN is your company's domain.
* Depending on your Linux distribution, localtime and timezone volume may not be necessary.
```
docker run -id \
  -h postfix --name postfix \
  --restart always \
  -v /etc/localtime:/etc/localtime:ro \
  -v /etc/timezone:/etc/timezone:ro \
  -p 25:25 \
  -e RELAYHOST=smtp.gmail.com \
  -e RELAYHOST_PORT=587 \
  -e RELAYHOST_USER=your-gmail-id \
  -e RELAYHOST_PASSWORD=your-gmail-app-password \
  -e MYHOSTNAME=my-domain.com \
  -e INET_INTERFACE=all \
  -e MYNETWORK_STYLE=host \
  -e MYNETWORKS="172.15.0.0/24 192.168.1.0/24" \
  -e MYMAILHOST=smtp-your-domain.com \
  -e MYDOMAIN=your-domain.com \
  alpine/postfix:homebrew 

```
