# Postfix Gmail Relay 

*Before setting up, you need to login to GMAIL to setup Application password.*
https://support.plesk.com/hc/en-us/articles/115004947113-How-to-set-up-Postfix-to-send-emails-using-Gmail-Relay-with-authentication-

## Docker build
```
docker build -t "alpine-postfix:homebrew" .
```

## Docker run
```
docker run -it \
  -h postfix --name postfix \
  --restart always \
  -v /etc/localtime:/etc/localtime:ro \
  -v /etc/timezone:/etc/timezone:ro \
  -p 25:25 \
  -e MYHOSTNAME my-domain.com \
  
  
 


```
