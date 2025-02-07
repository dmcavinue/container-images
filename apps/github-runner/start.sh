#!/bin/bash

REPO=$REPO
TOKEN=$TOKEN
NAME=$NAME

cd /home/github/actions-runner || exit
./config.sh --url https://github.com/${REPO} --token ${TOKEN} --name ${NAME}

cleanup() {
  echo "Removing runner..."
  ./config.sh remove --unattended --token ${TOKEN}
}

trap 'cleanup; exit 130' INT
trap 'cleanup; exit 143' TERM

./run.sh & wait $!