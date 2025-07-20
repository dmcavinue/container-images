FROM alpine:3

ENV TFTPD_EXTRA_ARGS=""

RUN apk add --no-cache tftp-hpa

RUN mkdir /tmp/syslinux && \
    wget "https://dl-cdn.alpinelinux.org/alpine/v3.19/main/x86_64/syslinux-6.04_pre1-r15.apk" -O /tmp/syslinux/syslinux.apk && \
    tar -C /tmp/syslinux -xvf /tmp/syslinux/syslinux.apk && \
    mkdir -p -m 0755 /tftpboot && \
    cp -r /tmp/syslinux/usr/share/syslinux /tftpboot && \
    rm -rf /tmp/syslinux && \
    find /tftpboot -type f -exec chmod 444 {} \;  && \
    find /tftpboot -mindepth 1 -type d -exec chmod 555 {} \;  && \
    ln -s ../boot /tftpboot/syslinux/boot && \
    ln -s ../pxelinux.cfg /tftpboot/syslinux/pxelinux.cfg && \
    ln -s ../boot /tftpboot/syslinux/efi64/boot && \
    ln -s ../pxelinux.cfg /tftpboot/syslinux/efi64/pxelinux.cfg

COPY pxelinux.cfg /tftpboot/pxelinux.cfg

EXPOSE 1069/udp
VOLUME /tftpboot/boot

CMD set -eu ;\
    [ -d /tftpboot/boot/root ] && cp -af /tftpboot/boot/root/* /tftpboot ;\
    exec in.tftpd -L -vvv -u ftp --secure --address "0.0.0.0:69" $TFTPD_EXTRA_ARGS /tftpboot
