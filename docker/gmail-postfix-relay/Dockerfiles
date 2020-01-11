FROM alpine:edge

RUN apk add --no-cache bash postfix postfix-pcre rsyslog ca-certificates gettext

COPY config /root/
RUN chmod -R 755 /root/config

EXPOSE 25

WORKDIR /root

ENTRYPOINT ["/root/config/entrypoint-postfix.sh"]
CMD ["startup"] 
