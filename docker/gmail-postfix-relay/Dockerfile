FROM alpine:edge

RUN apk add --no-cache bash postfix postfix-pcre rsyslog ca-certificates gettext

RUN mkdir /root/config

COPY config/init-postfix.sh /root/config/init-postfix.sh
COPY config/postfix-main.cf /root/config/postfix-main.cf
COPY config/postfix-sasl_passwd	/root/config/postfix-sasl_passwd
COPY config/startup-postfix.sh /root/config/startup-postfix.sh

RUN chmod -R 755 /root/config

EXPOSE 25

WORKDIR /root

ENTRYPOINT ["/root/config/entrypoint-postfix.sh"]
CMD ["startup"] 
