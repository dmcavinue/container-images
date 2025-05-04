FROM python:3

ARG USER=findmy
ARG USER_ID=10001
ARG WORKDIR="/opt/findmy"

USER root

RUN apt-get update && apt-get -y --no-install-recommends install sqlite3 \
&& mkdir -p /opt/findmy \
&& groupadd -f -g ${USER_ID} ${USER} \
&& useradd -l -u ${USER_ID} -g ${USER_ID} -d ${WORKDIR} -r ${USER} \
&& chown -R ${USER_ID}:${USER_ID} ${WORKDIR} \
&& chmod -R g+rwx ${WORKDIR}

USER $USER
