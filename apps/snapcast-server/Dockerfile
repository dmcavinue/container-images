FROM debian:stable-slim

ARG USER_UID=10001
ARG USER_GID=10001

RUN apt-get update && apt-get install -y --no-install-recommends \
    snapserver \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

RUN groupadd -g ${USER_GID} snapcast && \
    useradd -u ${USER_UID} -g snapcast -m -s /bin/bash snapcast && \
    chown -R ${USER_UID}:${USER_GID} /home/snapcast

WORKDIR /home/snapcast

USER snapcast

EXPOSE 1704 1705

ENTRYPOINT ["snapserver"]
