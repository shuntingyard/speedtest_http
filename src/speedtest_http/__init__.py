# -*- coding: utf-8 -*-

"""
The module to be launched as Flask app - spins up the things necessary
to serve plots over http.
"""

import logging
import os
import sys

import speedtest_reader

from flask import Flask
from flask.logging import default_handler

from logging.handlers import TimedRotatingFileHandler
from pkg_resources import get_distribution
from pkg_resources import DistributionNotFound

__author__ = "Tobias Frei"
__copyright__ = "Tobias Frei"
__license__ = "mit"

try:
    dist_name = __name__
    __version__ = get_distribution(dist_name).version
except DistributionNotFound:
    __version__ = "unknown"
finally:
    del get_distribution, DistributionNotFound

# Flask init 
app = Flask(__name__)

# env or last-resort defaults
INFILE = os.environ.get("INFILE", "./speedtest.csv")
TZ = os.environ.get("TZ", None)
LOGDIR = os.environ.get("LOGDIR", ".")
SITENAME = os.environ.get("SITENAME", None)

# to be imported late, after flask app initialization
from speedtest_http import views

# logging settings
FMT_LOGFILE = "[%(asctime)s] %(levelname)s: %(name)s: %(message)s"
FMT_CONSOLE = "[%(asctime)s] %(message)s"

# remove it when logging is initialized after the flask app
app.logger.removeHandler(default_handler)

if app.debug:
    # add streaming handler
    sh = logging.StreamHandler(sys.stdout)
    sh.setLevel(logging.DEBUG)
    sh.setFormatter(logging.Formatter(FMT_CONSOLE))
    app.logger.addHandler(sh)

    # TODO make this configurable.
    l2 = logging.getLogger("speedtest_reader.reader")
    l2.setLevel(logging.DEBUG)
    l2.addHandler(sh)
else:
    fh = TimedRotatingFileHandler(
        os.path.join(LOGDIR, "speedtest_http.log"), "midnight"
    )
    fh.setLevel(logging.INFO)
    fh.setFormatter(logging.Formatter(FMT_LOGFILE))
    app.logger.setLevel(logging.INFO)  # set to WARNING by default
    app.logger.addHandler(fh)

    # TODO make this configurable.
    l2 = logging.getLogger("speedtest_reader.reader")
    l2.setLevel(logging.INFO)
    l2.addHandler(fh)

# Say how we were started - but only once, hence this condition:
if not app.debug or os.environ.get("WERKZEUG_RUN_MAIN") == "true":

    # For now list all loggers to stdout when debugging.
    if True:  # app.debug:
        for name, obj in logging.root.manager.loggerDict.items():
            if isinstance(obj, logging.Logger):
                print(f"{name:36s} {obj}")

    msg = [
        "STARTING UP",
        f" speedtest_http:   {__version__}",
        f" speedtest_reader: {speedtest_reader.__version__}",
        f" INFILE:           {INFILE}",
        f" TZ:               {TZ}",
        f" LOGDIR:           {LOGDIR}",
        f" SITENAME          {SITENAME}",
    ]
    for line in msg:
        app.logger.info(line)
