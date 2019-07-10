FROM alpine:latest

ENV USER=pytester
ENV UID=2000
ENV GID=2000

RUN apk add --update --no-progress nfs-utils tzdata bash sudo python python-dev py-pip build-essential && \
        chmod +x /start.sh && \
        rm -rf /var/cache/apk/* \
        addgroup --gid "$GID" "$USER" \
        && adduser \
        --disabled-password \
        --gecos "" \
        --home "$(pwd)" \
        --ingroup "$USER" \
        --no-create-home \
        --uid "$UID" \
        "$USER"
