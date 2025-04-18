
FROM ghcr.io/tronbyt/pixlet:latest AS pixlet
FROM ghcr.io/tronbyt/server:main AS tronbyt

FROM debian:trixie-slim AS runtime

EXPOSE 8000

ENV PYTHONUNBUFFERED=1
ENV LIBPIXLET_PATH=/usr/lib/libpixlet.so

WORKDIR /app

COPY --from=pixlet --chmod=755 /lib/libpixlet.so /usr/lib/libpixlet.so

RUN apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        ca-certificates \
        esptool \
        git \
        gunicorn \
        libsharpyuv0 \
        libwebp7 \
        libwebpdemux2 \
        libwebpmux3 \
        python3 \
        python3-dotenv \
        python3-flask \
        python3-flask-babel \
        python3-pip \
        python3-requests \
        python3-tzlocal \
        python3-yaml \
        tzdata \
        tzdata-legacy && \
        pip3 install --no-cache-dir --root-user-action=ignore --break-system-packages flask-sock && \
        rm -rf /root/.cache/pip && \
        apt-get -y purge python3-pip && \
        apt-get -y autoremove && \
        rm -rf /var/lib/apt/lists/* /usr/lib/python3/dist-packages/pip /usr/bin/pip3

COPY --from=tronbyt /app /app

RUN pybabel compile -d tronbyt_server/translations

RUN useradd -ms /bin/bash -u 10001 tronbyt && chown -R 10001:10001 /app

USER tronbyt 

CMD ["./run"]