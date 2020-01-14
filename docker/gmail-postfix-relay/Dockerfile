FROM alpine:edge

RUN apk add --no-cache bash postfix postfix-pcre rsyslog ca-certificates gettext

RUN mkdir /root/WORKSPACE
WORKDIR /root/WORKSPACE

COPY init-postfix.sh /root/WORKSPACE/init-postfix.sh
COPY postfix-main.cf /root/WORKSPACE/postfix-main.cf
COPY postfix-sasl_passwd /root/WORKSPACE/postfix-sasl_passwd
COPY startup-postfix.sh /root/WORKSPACE/startup-postfix.sh

RUN chmod -R 755 /root/WORKSPACE

EXPOSE 25

ENTRYPOINT ["/root/WORKSPACE/init-postfix.sh"]
CMD ["startup"] 
