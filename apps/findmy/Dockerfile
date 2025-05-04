FROM dadoum/anisette-v3-server AS anisette

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

USER ${USER}

WORKDIR ${WORKDIR}

COPY --from=anisette /opt/anisette-v3-server /usr/local/bin/anisette-v3-server
COPY ./requirements.txt /tmp/requirements.txt

RUN git clone https://github.com/Dadoum/pyprovision.git && \
    cd ./pyprovision && \
    curl -fsS https://dlang.org/install.sh | bash -s ldc && \
    . ~/dlang/ldc-1.40.1/activate && \
    python -m pip install .

RUN git clone https://github.com/biemster/FindMy && \
    cd ./FindMy && \
    pip3 install -r /tmp/requirements.txt

WORKDIR ${WORKDIR}/FindMy