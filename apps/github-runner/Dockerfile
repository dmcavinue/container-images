FROM docker.io/mikefarah/yq:4.34.1 as yq

FROM docker:27-dind-rootless

ARG RUNNER_VERSION="2.322.0"
ARG DEBIAN_FRONTEND=noninteractive

USER root

RUN apk --update --no-cache add \
    dotnet9-sdk aspnetcore9-runtime dotnet9-runtime bash curl alpine-sdk python3 python3-dev py3-pip jq git

# libssl-dev libffi-dev ssh python3-venv python3-pip 

RUN curl -fsSL "https://github.com/go-task/task/releases/download/v3.41.0/task_linux_amd64.tar.gz" | tar xvz --overwrite --file - --directory /tmp \
    && mv /tmp/task /usr/local/bin/task \
    && chmod +x /usr/local/bin/task

COPY --from=yq /usr/bin/yq /usr/local/bin/yq

RUN cd /home/rootless && mkdir actions-runner && cd actions-runner \
    && curl -o actions-runner-linux-x64-${RUNNER_VERSION}.tar.gz -L https://github.com/actions/runner/releases/download/v${RUNNER_VERSION}/actions-runner-linux-x64-${RUNNER_VERSION}.tar.gz \
    && tar xzf actions-runner-linux-x64-${RUNNER_VERSION}.tar.gz

RUN chown -R rootless /home/rootless 
# && /home/rootless/actions-runner/bin/installdependencies.sh

COPY start.sh /start.sh
RUN chmod +x /start.sh

USER rootless

ENTRYPOINT ["/start.sh"]