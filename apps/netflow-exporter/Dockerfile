FROM alpine:3
RUN apk add --no-cache pmacct jq && \
    addgroup -g 10001 nfacctd && \
    adduser --system --disabled-password \
    --home /usr/share/nfacctd \
    --uid 10001 --ingroup nfacctd nfacctd

COPY nfacctd.conf /etc/pmacct/nfacctd.conf

USER nfacctd

ENTRYPOINT ["nfacctd"]

CMD ["-f", "/etc/pmacct/nfacctd.conf"]