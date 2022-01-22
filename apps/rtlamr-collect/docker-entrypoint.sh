#!/bin/sh

echo "Starting rtl_tcp..."
rtl_tcp &

sleep 30

rtlamr | rtlamr-collect