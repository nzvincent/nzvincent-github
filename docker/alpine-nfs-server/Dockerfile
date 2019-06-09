FROM alpine:latest

ADD start.sh /start.sh

RUN     apk add --update --no-progress nfs-utils && \
        chmod +x /start.sh && \
        rm -rf /var/cache/apk/*

EXPOSE 111/udp 2049/tcp

CMD ["/start.sh"]
