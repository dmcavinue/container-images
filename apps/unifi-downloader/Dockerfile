FROM unifitoolbox/protect-archiver:2.3.3

COPY docker-entrypoint.sh /
RUN chmod +x /docker-entrypoint.sh

RUN apt-get update && apt-get install -y \
  rclone \
  && rm -rf /var/lib/apt/lists/*

RUN mkdir /download
WORKDIR /download
VOLUME [ "/download" ]

ENTRYPOINT ["/docker-entrypoint.sh"]
