FROM ghcr.io/music-assistant/server:latest

RUN adduser --gecos "" --disabled-password --uid 1001 app \
    && mkdir /data \
    && chown -R app:app /app \
    && chown -R app:app /data

USER app