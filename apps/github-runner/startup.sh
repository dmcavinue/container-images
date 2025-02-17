#!/bin/bash

REPO=$REPO
TOKEN=$TOKEN
NAME=$NAME

sudo /bin/bash <<SCRIPT
mkdir -p /etc/docker

if [ ! -f /etc/docker/daemon.json ]; then
  echo "{}" > /etc/docker/daemon.json
fi

if [ -n "${MTU}" ]; then
jq ".\"mtu\" = ${MTU}" /etc/docker/daemon.json > /tmp/.daemon.json && mv /tmp/.daemon.json /etc/docker/daemon.json
# See https://docs.docker.com/engine/security/rootless/
export DOCKERD_ROOTLESS_ROOTLESSKIT_MTU=${MTU}
fi
SCRIPT

sudo /usr/bin/dockerd &

processes=(dockerd)

for process in "${processes[@]}"; do
    if ! wait_for_process "$process"; then
        echo "$process is not running after max time"
        exit 1
    else
        echo "$process is running"
    fi
done

if [ -n "${MTU}" ]; then
  sudo ifconfig docker0 mtu "${MTU}" up
fi

cd /runnertmp/ || exit
./config.sh --url https://github.com/${REPO} --token ${TOKEN} --name ${NAME}

cleanup() {
  echo "Removing runner..."
  ./config.sh remove --unattended --token ${TOKEN}
}

trap 'cleanup; exit 130' INT
trap 'cleanup; exit 143' TERM

./run.sh & wait $!