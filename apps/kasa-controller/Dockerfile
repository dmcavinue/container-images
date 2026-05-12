FROM python:3.12-slim

ARG UID=10001
ARG GID=10001
ARG USER=appuser

RUN apt-get update \
 && apt-get upgrade -y \
 && rm -rf /var/lib/apt/lists/*

RUN groupadd -g ${GID} ${USER} \
 && useradd  -u ${UID} -g ${GID} -m -s /usr/sbin/nologin ${USER}

ENV VENV_PATH=/opt/venv
RUN python -m venv ${VENV_PATH} \
 && chown -R ${USER}:${USER} ${VENV_PATH}

USER ${USER}

WORKDIR /app

ENV PATH="${VENV_PATH}/bin:$PATH"
ENV TZ=America/New_York

COPY --chown=${USER}:${USER} requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY --chown=${USER}:${USER} app.py /app/app.py

ENV PYTHONUNBUFFERED=1
EXPOSE 8080

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8080"]