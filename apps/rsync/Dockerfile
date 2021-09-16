FROM alpine:3.13.5

RUN apk add --update-cache \
    rsync \
    openssh-client \
    tzdata \
 && rm -rf /var/cache/apk/*

ENTRYPOINT [ "rsync" ]