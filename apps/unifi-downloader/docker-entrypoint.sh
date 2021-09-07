#!/bin/sh

# UNIFI_HOST="192.168.1.1"
# UNIFI_USER="unifi-downloader"
# UNIFI_PWD="xxxxxxxx"
# OUTPUT_DIR="/mnt/data/cctv"

MINUTES=${MINUTES:-5}
START_TIME=$(date -u -d "$date -${MINUTES} mins" +"%Y-%m-%dT%H:%M:%S")
CURRENT_TIME=$(date -u -d "$date -0 mins" +"%Y-%m-%dT%H:%M:%S")

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
