FROM dadoum/anisette-v3-server AS anisette

FROM python:3

ARG USER=anisette-server
ARG USER_ID=10001
ARG WORKDIR="/opt/findmy"

USER root

RUN mkdir -p ${WORKDIR} \
&& groupadd -f -g ${USER_ID} ${USER} \
&& useradd -l -u ${USER_ID} -g ${USER_ID} -d ${WORKDIR} -r ${USER} \
&& chown -R ${USER_ID}:${USER_ID} ${WORKDIR} \
&& chmod -R g+rwx ${WORKDIR}

COPY --from=anisette /opt/anisette-v3-server /usr/local/bin/anisette-v3-server

USER ${USER}
WORKDIR ${WORKDIR}

ENTRYPOINT ["anisette-v3-server"]