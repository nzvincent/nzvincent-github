FROM debian:latest

ENV USER=pytester
ENV UID=2000
ENV GID=2000

RUN apt-get update && apt-get upgrade && \
    apt-get -y install sudo git python python-dev python-pip  && \
    addgroup --gid "$GID" "$USER" \
    && adduser \
    --disabled-password \
    --gecos "" \
    --home "$(pwd)" \
    --ingroup "$USER" \
    --uid "$UID" \
    "$USER"
