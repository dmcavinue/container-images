FROM python:3

WORKDIR /usr/src

RUN \
    apt-get update \
    && apt-get install -y --no-install-recommends \
        netcat \
        python3 \
        python3-pip \
    \
    && pip3 install --no-cache-dir -U \
        setuptools \
        wheel \
    && pip3 install --no-cache-dir \
        "wyoming-piper==0.0.2" \
    \
    && curl -L -s \
        "https://github.com/rhasspy/piper/releases/download/v0.0.2/piper_amd64.tar.gz" \
        | tar -zxvf - -C /usr/share \
    \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /

HEALTHCHECK --start-period=10m \
    CMD echo '{ "type": "describe" }' \
        | nc -w 1 localhost 10200 \
        | grep -q "piper" \
        || exit 1