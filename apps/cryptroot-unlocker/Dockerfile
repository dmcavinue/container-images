FROM alpine:3

ARG USER=unlocker
ENV HOME /home/$USER

RUN apk update && apk add --no-cache openssh netcat-openbsd && \
    apk upgrade -U

RUN adduser -D $USER

COPY entrypoint.sh .

RUN chmod +x /entrypoint.sh

USER $USER

RUN mkdir -p /home/$USER/.ssh

ENTRYPOINT ["/entrypoint.sh"]