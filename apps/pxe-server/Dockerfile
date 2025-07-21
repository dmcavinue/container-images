FROM alpine:3

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

#COPY pxelinux.cfg /tftpboot/pxelinux.cfg

# Support clients that use backslash instead of forward slash.
COPY mapfile /tftpboot/

EXPOSE 69/udp
VOLUME /tftpboot/boot

RUN adduser --system --disabled-password \
    --home /usr/share/tftp \
    --uid 10001 tftp

COPY start /usr/sbin/start
RUN chmod +x /usr/sbin/start

ENTRYPOINT ["/usr/sbin/start"]
CMD ["-L", "--verbose", "-m", "/tftpboot/mapfile", "-u", "tftp", "--secure", "--blocksize", "1468", "/tftpboot"]