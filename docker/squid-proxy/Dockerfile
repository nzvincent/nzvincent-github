FROM alpine:edge

RUN apk add --no-cache bash nano squid acf-squid openrc
RUN apk update ca-certificates

RUN mkdir /root/WORKSPACE
WORKDIR /root/WORKSPACE

COPY init-squid.sh /root/WORKSPACE/init-squid.sh

EXPOSE 3128 80 443

ENTRYPOINT ["/root/WORKSPACE/init-squid.sh"]
#CMD ["startup"] 
