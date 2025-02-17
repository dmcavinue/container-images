FROM docker.io/mikefarah/yq:4.34.1 as yq

FROM summerwind/actions-runner-dind-rootless:v2.316.0-ubuntu-22.04

ARG DEBIAN_FRONTEND=noninteractive

USER root

RUN curl -fsSL "https://github.com/go-task/task/releases/download/v3.41.0/task_linux_amd64.tar.gz" | tar xvz --overwrite --file - --directory /tmp \
    && mv /tmp/task /usr/local/bin/task \
    && chmod +x /usr/local/bin/task

COPY --from=yq /usr/bin/yq /usr/local/bin/yq

COPY start.sh /start.sh
RUN chmod +x /start.sh

USER runner

ENTRYPOINT ["/start.sh"]