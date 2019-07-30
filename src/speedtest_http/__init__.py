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
from speedtest_reader import logger as reader_logger

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
INFILE = os.environ.get("INFILE", os.path.join(os.getcwd(), "tests/min.csv"))
TZ = os.environ.get("TZ", None)
LOGDIR = os.environ.get("LOGDIR", ".")
SITENAME = os.environ.get("SITENAME", None)

# logging settings
FMT_LOGFILE = "[%(asctime)s] %(levelname)-8s %(name)s: %(message)s"
FMT_CONSOLE = "[%(asctime)s] %(name)s: %(message)s"

# remove when logging is initialized after the flask app
app.logger.removeHandler(default_handler)

if app.debug:
    # add streaming handler
    sh = logging.StreamHandler(sys.stdout)
    sh.setLevel(logging.DEBUG)
    sh.setFormatter(logging.Formatter(FMT_CONSOLE))
    app.logger.addHandler(sh)

    # TODO make this configurable.
    reader_logger.setLevel(logging.DEBUG)
    reader_logger.addHandler(sh)
else:
    fh = TimedRotatingFileHandler(
        os.path.join(LOGDIR, "speedtest_http.log"), "midnight"
    )
    fh.setLevel(logging.INFO)
    fh.setFormatter(logging.Formatter(FMT_LOGFILE))
    app.logger.setLevel(logging.INFO)  # set to WARNING by default
    app.logger.addHandler(fh)

    # TODO make this configurable.
    reader_logger.setLevel(logging.INFO)
    reader_logger.addHandler(fh)

# Say how we were started - but only once, hence this condition:
if not app.debug or os.environ.get("WERKZEUG_RUN_MAIN") == "true":

    # For now list all loggers to stdout when debugging.
    if app.debug:
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

    # to be imported late, after flask app initialization
    from speedtest_http import views
