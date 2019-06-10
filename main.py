# -*- coding: utf-8 -*-

""" A module to be launched as Flask app - spins up the things necessary
to serve plots over http.

TODO improve (http status code) error handling from `dash` to `flask`!
"""

import logging
import os

# import sys

import dash
import dash_core_components as dcc
import dash_html_components as html

from dash.dependencies import Input
from dash.dependencies import Output
from flask import Flask
from flask import render_template
from flask import request

# production plots
from localpy import heatmap
from localpy import lineplot

# lab plots
from localpy import walktz

__author__ = "Tobias Frei"
__copyright__ = "Tobias Frei"
__license__ = "gpl2"

# settings from the environment
INFILE = os.environ["INFILE"]
TZ = os.environ["TZ"]
LOGDIR = os.environ["LOGDIR"]
SITENAME = os.environ["SITENAME"]


def _setup_logging(loglevel):
    """Setup basic logging - with `logformat` werkzeug-like.
    """
    logformat = "%(levelname)s:%(name)s: [%(asctime)s] %(message)s"
    logging.basicConfig(
        level=loglevel,
        # stream=sys.stdout,
        filename=LOGDIR + "/flask.log",
        format=logformat,
        datefmt="%Y-%m-%d %H:%M:%S",
    )


def _announce():
    """Write first message to stdout and log.
    """
    if not _srv.debug or os.environ.get("WERKZEUG_RUN_MAIN") == "true":
        # app not in debug mode or we are in the reloaded process
        msg = f"Up with: INFILE={INFILE} TZ={TZ} LOGDIR={LOGDIR} SITENAME={SITENAME}"

        if _srv.debug:
            _setup_logging("DEBUG")
        else:
            _setup_logging("INFO")

        _logger.info(msg)


# define flask server
_srv = Flask(
    __name__,
    # template_folder="../../templates/",
)
_logger = logging.getLogger(__name__)
_announce()


@_srv.route("/")
def _index():
    """Render index page.
    """
    env = request.__dict__["environ"]
    msg = "Requesting index with:"
    for key in env:
        if "REMOTE" in key or "HTTP_US" in key:
            msg = msg + f" {key}={env[key]}"
    _logger.debug(msg)
    return render_template("index.html", sitename=SITENAME)


@_srv.errorhandler(404)
def _http404(e):
    return render_template("404.html"), 404


# define hosted dash app
_external_stylesheets = ["https://codepen.io/chriddyp/pen/bWLwgP.css"]
app = dash.Dash(
    __name__,
    external_stylesheets=_external_stylesheets,
    meta_tags=[
        {"name": "viewport", "content": "width=device-width, initial-scale=1"}
    ],
    server=_srv,
    routes_pathname_prefix="/data/",
)

app.title = SITENAME
app.layout = html.Div(
    [dcc.Location(id="url", refresh=False), html.Div(id="page-content")]
)


@app.callback(Output("page-content", "children"), [Input("url", "pathname")])
def _route(pathname):
    """Route to dash plots.
    """
    _logger.debug(f"Serving route: {pathname}")
    if pathname == "/data/lineplot_today":
        return lineplot.layout(
            INFILE, TZ, SITENAME, shorthand="from_midnight"
        )
    elif pathname == "/data/lineplot_last24hours":
        return lineplot.layout(
            INFILE, TZ, SITENAME, shorthand="last24hours"
        )
    elif pathname == "/data/heatmap_last30days":
        return heatmap.layout(
            INFILE, TZ, SITENAME, shorthand="last30days"
        )
    elif pathname == "/data/walktz":
        return walktz.layout()
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
            # It's normally `None` on the first callback.
            return
