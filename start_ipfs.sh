#! /bin/bash
set -e
if [ ! -z "$1" ]; then
    GOLOG_FILE="$1"
else
    GOLOG_FILE=ipfs.log
fi

if [ ! -z "$2" ]; then
    IPFS_CMD="$2"
else
    IPFS_CMD=ipfs
fi
GOLOG_FILE=$GOLOG_FILE GOLOG_LOG_FMT=json GOLOG_OUTPUT=stdout+file GOLOG_LOG_LEVEL=error,provider.simple=info,provider.queue=info,reprovider.simple=info,bitswap=debug $IPFS_CMD daemon --enable-pubsub-experiment --upgrade-cidv0-in-output