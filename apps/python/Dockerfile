FROM python:3

ARG USER=python
ARG USER_ID=10001
ARG WORKDIR="/app"

USER root

ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update -y \
&& apt-get install -y --no-install-recommends \
    curl \
    ca-certificates \
    git \
    nano \
    jq \
    unzip \
    zip \
    && rm -rf /var/lib/apt/lists/* \
&& mkdir -p ${WORKDIR} \
&& groupadd -f -g ${USER_ID} ${USER} \
&& useradd -l -u ${USER_ID} -g ${USER_ID} -d ${WORKDIR} -r ${USER} \
&& chown -R ${USER_ID}:${USER_ID} ${WORKDIR} \
&& chmod -R g+rwx ${WORKDIR}

USER ${USER}
WORKDIR ${WORKDIR}
