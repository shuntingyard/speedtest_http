#!/bin/sh

# set environment for app
export TZ=Europe/Zurich
export INFILE=/data/speedtest.csv
export LOGDIR=/data/log
export SITENAME="Uplink green.ch"

# set environment for flask
export FLASK_APP=speedtest_http
export FLASK_DEBUG=0
python -m flask run -h 0.0.0.0  # -p 8050
