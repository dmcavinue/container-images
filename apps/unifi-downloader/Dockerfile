FROM python:latest

ARG PROTECT_VERSION=2.0.2

RUN pip install "https://github.com/unifi-toolbox/unifi-protect-video-downloader/releases/download/v${PROTECT_VERSION}/protect_archiver-2.0.2-py3-none-any.whl"

COPY docker-entrypoint.sh /
RUN chmod +x /docker-entrypoint.sh

RUN mkdir /download
WORKDIR /download
VOLUME [ "/download" ]

ENTRYPOINT ["/docker-entrypoint.sh"]
