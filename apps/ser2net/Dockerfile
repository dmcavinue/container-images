FROM alpine:3.19
RUN apk add --no-cache ser2net && \
    adduser --system --disabled-password \
    --home /usr/share/ser2net \
    --uid 1001 --ingroup dialout ser2net

COPY ser2net.conf /etc/ser2net.conf

USER ser2net

ENTRYPOINT ["ser2net", "-d", "-c", "/etc/ser2net.conf"]