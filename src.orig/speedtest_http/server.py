# -*- coding: utf-8 -*-
"""
A module to be launched as Flask app - spins up the things necessary
to serve plots over http.

TODO improve (http status code) error handling from `dash` to `flask`!
"""

import logging
import os

# import sys
# import traceback

import dash
import dash_core_components as dcc
import dash_html_components as html
import speedtest_reader

from dash.dependencies import Input
from dash.dependencies import Output
from flask import Flask
from flask import render_template
from flask import request

# production plots
from speedtest_http import heatmap
from speedtest_http import lineplot

__author__ = "Tobias Frei"
__copyright__ = "Tobias Frei"
__license__ = "mit"

# Get environment settings.
INFILE = os.environ["INFILE"]
TZ = os.environ["TZ"]
LOGDIR = os.environ["LOGDIR"]
SITENAME = os.environ["SITENAME"]


def _setup_logging(loglevel):
    """Setup basic logging."""
    logging.basicConfig(
        level=loglevel,
        filename=LOGDIR + "/flask.log",
        format="[%(asctime)s] %(levelname)s: %(name)s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )


def _initialize():
    """Log our start and load data store."""
    # Flask is not in debug mode or we are in the reloaded process.
    if not _srv.debug or os.environ.get("WERKZEUG_RUN_MAIN") == "true":

        # For now list all loggers to stdout, when in debug mode.
        if _srv.debug:
            for name, attributes in logging.root.manager.loggerDict.items():
                print(f"{name:24s} {attributes}")

        msg = [
            "STARTING UP",
            f" speedtest_reader: {speedtest_reader.__version__}",
            f" INFILE={INFILE}",
            f" TZ={TZ}",
            f" LOGDIR={LOGDIR}",
            f" SITENAME={SITENAME}",
            f" dash version: {dash.__version__}",
            "LOADING DATA STORE",
        ]
        for line in msg:
            _srv.logger.info(line)
            print(line)


# Define the flask server.
_srv = Flask(
    __name__,
    template_folder="../templates/",
)

# Configure the logger.
if _srv.debug:
    _setup_logging("DEBUG")
else:
    _setup_logging("INFO")

# Run som things only once, even when reloading/ debugging.
_initialize()


@_srv.route("/")
def _index():
    """Render index page."""

    # Access some request attributes.
    env = request.__dict__["environ"]
    msg = "Requesting index with:"
    for key in env:
        if "REMOTE" in key or "HTTP_US" in key:
            msg = msg + f" {key}={env[key]}"
    _srv.logger.debug(msg)

    return render_template("index.html", sitename=SITENAME)


@_srv.errorhandler(404)
def _http404_e(e):
    return render_template("404.html"), 404


# @_srv.errorhandler(Exception)
# def _general_e(e):
#     _, value, tb = sys.exc_info()
#     _srv.logger.error(value)
#     _srv.logger.error(f"TRACE: {traceback.print_tb(tb)}")
#     return (
#         render_template(
#             "exception.html", text=value, trace=traceback.print_tb(tb)
#         ),
#         500,
#     )


# Define the hosted dash app.
_external_stylesheets = ["https://codepen.io/chriddyp/pen/bWLwgP.css"]
app = dash.Dash(
    __name__,
    external_stylesheets=_external_stylesheets,
    meta_tags=[
        {"name": "viewport", "content": "width=device-width, initial-scale=1"}
    ],
    server=_srv,
    # Routing prefix for all inside the hosted app.
    routes_pathname_prefix="/data/",
)
app.title = SITENAME
app.layout = html.Div(
    [dcc.Location(id="url", refresh=False), html.Div(id="page-content")]
)


@app.callback(Output("page-content", "children"), [Input("url", "pathname")])
def _route(pathname):
    """Route to dash plots."""

    _srv.logger.debug(f"Serving route: {pathname}")

    if pathname == "/data/lineplot_today":
        return lineplot.layout(INFILE, TZ, SITENAME, mnemonic="from_midnight")
    elif pathname == "/data/lineplot_last24hours":
        return lineplot.layout(INFILE, TZ, SITENAME, start="24 hours ago")
    elif pathname == "/data/heatmap_last30days":
        return heatmap.layout(INFILE, TZ, SITENAME, start="30 days ago")

    else:
        if pathname:
            # TODO stash this away to a helper file!
            # TODO or can this be rendered from templates?

            # Don't see how to set a http status 404 AND render the page -
            # raising flask abort(404) will not render, succesful
            # rendering will return http status 200.
            return html.Div(
                [
                    html.H3("404"),
                    html.H2("Not Found"),
                    html.H1("Just look somwhere else ¯\\_(°.°)_/¯"),
                ]
            )
        else:
            # Pathname is always `None` on the first callback.
            return
