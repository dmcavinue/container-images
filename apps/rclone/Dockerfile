FROM alpine:3.13.5

RUN apk add --update-cache \
    rclone \
 && rm -rf /var/cache/apk/*

ENTRYPOINT [ "rclone" ]