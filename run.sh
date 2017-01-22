#!/usr/bin/env bash

PYTHON_VERSION="3.6"
PROGRAM_DIR="crawler"
PROGRAM="01_async.py"

if [[ $# -ge 1 ]]; then
    if [[ -f ${PROGRAM_DIR}/$1 ]]; then
        PROGRAM=$1
    else
        echo "File $1 not found!"
        exit 1
    fi
fi

echo "Running $PROGRAM on Python $PYTHON_VERSION"
docker run \
    --rm \
    -v ${PWD}/${PROGRAM_DIR}:/app/${PROGRAM_DIR} \
    -e PYTHONPATH=/app/ \
    python:$PYTHON_VERSION \
    python /app/${PROGRAM_DIR}/${PROGRAM}
