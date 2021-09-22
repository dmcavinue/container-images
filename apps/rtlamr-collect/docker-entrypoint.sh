#!/bin/sh

echo "Starting rtl_tcp..."
rtl_tcp &

rtlamr | rtlamr-collect