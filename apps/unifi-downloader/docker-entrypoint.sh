#!/bin/sh

MINUTES=${MINUTES:-5}
INTERVAL=${INTERVAL:-60}
OUTPUT_DIR=${OUTPUT_DIR:-"/download"}
BACKUP_DIR=${BACKUP_DIR:-"/backup"}

echo "host:${UNIFI_HOST}"

while :
do

  START_TIME=$(date -d "$date -${MINUTES} mins" +"%Y-%m-%dT%H:%M:%S")
  CURRENT_TIME=$(date -d "$date -0 mins" +"%Y-%m-%dT%H:%M:%S")

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

  rclone copy --max-age 10m ${OUTPUT_DIR} ${BACKUP_DIR}/unifi -v

  find ${OUTPUT_DIR} -type d -mtime +4 -exec rm -r "{}" \;

	sleep ${INTERVAL}
done