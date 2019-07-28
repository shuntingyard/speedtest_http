#!/bin/sh

# set environment for app
export TZ=Europe/Zurich
export INFILE=~/speedtest.csv
export LOGDIR=/data
export SITENAME="Uplink green.ch"

# set environment for flask
export FLASK_APP=speedtest_http
export FLASK_DEBUG=1
python -m flask run -h 0.0.0.0  # -p 8050
