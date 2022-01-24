#!/bin/sh

MINUTES=${MINUTES:-5}
START_TIME=$(date -u -d "$date -${MINUTES} mins" +"%Y-%m-%dT%H:%M:%S")
CURRENT_TIME=$(date -u -d "$date -0 mins" +"%Y-%m-%dT%H:%M:%S")
OUTPUT_DIR=${OUTPUT_DIR:-"/download"}

echo "host:${UNIFI_HOST}"

protect-archiver \
  events \
  --address "${UNIFI_HOST}" \
  --username "${UNIFI_USER}" \
  --password "${UNIFI_PWD}" \
  --skip-existing-files \
  --start "${START_TIME}" \
  --end "${CURRENT_TIME}" \
  --ignore-failed-downloads \
  --download-motion-heatmaps \
  ${OUTPUT_DIR}

find ${OUTPUT_DIR} -type d -mtime +4 -exec rm -r "{}" \;