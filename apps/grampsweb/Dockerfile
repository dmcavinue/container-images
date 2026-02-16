FROM ghcr.io/gramps-project/grampsweb:26.2.0

RUN apt-get update \
  && apt-get upgrade -y \
  && rm -rf /var/lib/apt/lists/*

ARG UID=10001
ARG GID=10001

RUN groupadd -g ${GID} grampsweb \
  && useradd -m -u ${UID} -g grampsweb -s /usr/sbin/nologin grampsweb \
  && chown -R $UID:$GID /app /root /tmp

USER grampsweb
WORKDIR /app
ENV HOME=/app