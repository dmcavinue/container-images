#!/bin/sh
# polls a provided ssh host/port and runs a cryptroot unlock

POLLING_INTERVAL="${POLLING_INTERVAL:-120}"
SSH_TIMEOUT="${SSH_TIMEOUT:-30}"
SSH_USER="${SSH_USER:-root}"
SSH_PORT="${SSH_PORT:-22}"
SSH_IDENTITY_FILE="${SSH_IDENTITY_FILE:-~/.ssh/id_rsa}"

while true
do
  nc -z -w5 $SSH_HOST $SSH_PORT
  if [ "$?" -eq 0 ]; then
    echo "Unlocking ${SSH_HOST}:${SSH_PORT}"
    echo $CRYPTKEY | ssh -o ConnectTimeout=${SSH_TIMEOUT} "${SSH_USER}@${SSH_HOST}" -p $SSH_PORT -i "${SSH_IDENTITY_FILE}" cryptroot-unlock
  else
    echo "sleeping for ${POLLING_INTERVAL} seconds..."
  fi  
  sleep $POLLING_INTERVAL
done