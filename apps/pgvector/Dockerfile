FROM ghcr.io/cloudnative-pg/postgresql:15.5-5

USER root

RUN set -xe; \
	apt-get update; \
	apt-get install -y --no-install-recommends \
		"postgresql-15-pgvector" ; \
	rm -fr /tmp/* ; \
	rm -rf /var/lib/apt/lists/*;

USER 26