FROM ubuntu:22.04
ARG RUNNER_VERSION="2.322.0"
ARG DEBIAN_FRONTEND=noninteractive

RUN apt update -y && apt upgrade -y

RUN useradd -m github

RUN apt install -y --no-install-recommends \
    curl build-essential libssl-dev libffi-dev python3 python3-venv python3-dev python3-pip jq
RUN apt-get -yqq install ssh

RUN cd /home/github && mkdir actions-runner && cd actions-runner \
    && curl -o actions-runner-linux-x64-${RUNNER_VERSION}.tar.gz -L https://github.com/actions/runner/releases/download/v${RUNNER_VERSION}/actions-runner-linux-x64-${RUNNER_VERSION}.tar.gz \
    && tar xzf actions-runner-linux-x64-${RUNNER_VERSION}.tar.gz

RUN chown -R github /home/github && /home/github/actions-runner/bin/installdependencies.sh

COPY start.sh /start.sh
RUN chmod +x /start.sh

USER github

ENTRYPOINT ["/start.sh"]