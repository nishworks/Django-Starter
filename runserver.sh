#!/usr/bin/env bash

#Config
IP=127.0.0.1
PORT=4000
WORKERS=4

#Run gunicorn server
tox
source activate
gunicorn -w ${WORKERS} -b ${IP}:${PORT} voyage:voyage_app
