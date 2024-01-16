FROM actualbudget/actual-server:24.1.0-alpine

ARG USERNAME=appuser
ARG USER_UID=1001
ARG USER_GID=$USER_UID

RUN addgroup -S ${USERNAME} -g ${USER_GID} && adduser -S ${USERNAME} -G ${USERNAME} -u ${USER_UID} && \
    chown -R ${USERNAME}:${USERNAME} /app && \
    mkdir /data && chown -R ${USERNAME}:${USERNAME} /data

USER ${USER_UID}

ENTRYPOINT ["/sbin/tini","-g",  "--"]
EXPOSE 5006
CMD ["node", "app.js"]