FROM ghcr.io/cloudnative-pg/postgresql:15.5-5

USER root

ENV VECTORS_VERSION v0.1.11

RUN apt-get update && apt-get install -y wget && \
	wget https://github.com/tensorchord/pgvecto.rs/releases/download/${VECTORS_VERSION}/vectors-pg15-${VECTORS_VERSION}-x86_64-unknown-linux-gnu.deb -O /tmp/vectors.deb && \
	apt-get install -y /tmp/vectors.deb && rm -f /tmp/vectors.deb \
	rm -rf /tmp/* && \
	rm -rf /var/lib/apt/lists/*

USER 26