FROM unifitoolbox/protect-archiver:2.1.2

COPY docker-entrypoint.sh /
RUN chmod +x /docker-entrypoint.sh

RUN mkdir /download
WORKDIR /download
VOLUME [ "/download" ]

ENTRYPOINT ["/docker-entrypoint.sh"]
