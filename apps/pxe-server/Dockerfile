FROM alpine:3.13.5

ENV DHCP_RANGE 192.168.56.2
ENV MEMTEST_VERSION 5.01
ENV SYSLINUX_VERSION 6.03
ENV TMP_SYSLINUX_PATH /tmp/syslinux-"${SYSLINUX_VERSION}"

LABEL maintainer "dan@mcavinue.io"

RUN apk add --no-cache --update \
  dnsmasq \
  wget

WORKDIR /tmp

RUN \
  mkdir -p "${TMP_SYSLINUX_PATH}" \
  && wget -q https://www.kernel.org/pub/linux/utils/boot/syslinux/syslinux-"${SYSLINUX_VERSION}".tar.gz \
  && tar -xzf syslinux-"${SYSLINUX_VERSION}".tar.gz \
  && mkdir -p /var/lib/tftpboot \
  && cp "${TMP_SYSLINUX_PATH}"/bios/core/pxelinux.0 /var/lib/tftpboot/ \
  && cp "${TMP_SYSLINUX_PATH}"/bios/com32/libutil/libutil.c32 /var/lib/tftpboot/ \
  && cp "${TMP_SYSLINUX_PATH}"/bios/com32/elflink/ldlinux/ldlinux.c32 /var/lib/tftpboot/ \
  && cp "${TMP_SYSLINUX_PATH}"/bios/com32/menu/menu.c32 /var/lib/tftpboot/ \
  && rm -rf "${TMP_SYSLINUX_PATH}" \
  && rm /tmp/syslinux-"${SYSLINUX_VERSION}".tar.gz

# MemTest86+
RUN wget -q http://www.memtest.org/download/"${MEMTEST_VERSION}"/memtest86+-"${MEMTEST_VERSION}".bin.gz \
  && gzip -d memtest86+-"${MEMTEST_VERSION}".bin.gz \
  && mkdir -p /var/lib/tftpboot/memtest \
  && mv memtest86+-${MEMTEST_VERSION}.bin /var/lib/tftpboot/memtest/memtest86+

COPY etc/ /etc
COPY tftpboot/ /var/lib/tftpboot

ENTRYPOINT ["dnsmasq", "--no-daemon"]
CMD ["--dhcp-range=${DHCP_RANGE},proxy"]