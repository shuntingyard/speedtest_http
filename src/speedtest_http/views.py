# -*- coding: utf-8 -*-

"""
The V (as in MVC) module
"""

from flask import request
from flask import render_template

from speedtest_http import __version__
from speedtest_http import INFILE
from speedtest_http import SITENAME
from speedtest_http import TZ
from speedtest_http import app

# charts
from speedtest_http import gitau
from speedtest_http import plt_lineplot
from speedtest_http import plt_heatmap

__author__ = "Tobias Frei"
__copyright__ = "Tobias Frei"
__license__ = "mit"


@app.route("/")
def _index():
    return render_template(
        "index.html", sitename=SITENAME, version=__version__
    )


@app.route("/lineplot_today")
def lineplot_today():
    return render_template(
        "gt2.html",
        plot=plt_lineplot.layout(
            INFILE, TZ, SITENAME, mnemonic="from_midnight"
        ),
    )


@app.route("/lineplot_last24hours")
def lineplot_last24():
    return render_template(
        "gt2.html",
        plot=plt_lineplot.layout(INFILE, TZ, SITENAME, start="24 hours ago"),
    )


@app.route("/heatmap_last30days")
def heatmap():
    return render_template(
        "gt2.html",
        plot=plt_heatmap.plot(INFILE, TZ, SITENAME, start="30 days ago"),
    )


@app.route("/gitau")
def bars():
    """The example used to model the first pure plotly plot."""
    return render_template("gitau.html", plot=gitau.plot("Bar"))


@app.route("/gitau/sel", methods=["GET", "POST"])
def change_feature():
    """Endpoint for AJAX calls"""
    return gitau.plot(request.args["selected"])


@app.errorhandler(404)
def http404_e(e):
    """Not found"""
    return render_template("404.html"), 404
