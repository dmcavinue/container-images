FROM ghcr.io/cloudnative-pg/postgresql:15.5-5

USER root

ENV VECTORS_VERSION 0.2.0

RUN apt-get update && apt-get install -y wget && \
        wget https://github.com/tensorchord/pgvecto.rs/releases/download/$v{VECTORS_VERSION}/vectors-pg15_${VECTORS_VERSION}_amd64.deb -O /tmp/vectors.deb && \
	apt-get install -y /tmp/vectors.deb && rm -f /tmp/vectors.deb \
	rm -rf /tmp/* && \
	rm -rf /var/lib/apt/lists/*

USER 26
