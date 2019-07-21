# -*- coding: utf-8 -*-

"""
The V (as in MVC) module
"""

from flask import request
from flask import render_template
from speedtest_reader import format_timestamps, Reader, util

from speedtest_http import __version__
from speedtest_http import INFILE
from speedtest_http import SITENAME
from speedtest_http import TZ
from speedtest_http import app

# charts
from speedtest_http import gitau
from speedtest_http import plt_scatter
from speedtest_http import plt_heatmap

__author__ = "Tobias Frei"
__copyright__ = "Tobias Frei"
__license__ = "mit"


sensor1 = Reader(INFILE)


@util.append_tslocal()
@util.to_Mbit
def slice_s1(**kwargs):
    kwargs["tz"] = TZ
    start, end = format_timestamps(**kwargs)
    return sensor1.copy_df(start, end)


@app.route("/")
def _index():
    return render_template(
        "index.html", sitename=SITENAME, version=__version__
    )


@app.route("/lineplot_today")
def lineplot_today():
    return render_template(
        "gt2.html",
        plot=plt_scatter.plot(
            slice_s1(start="12 midnight"),
            title=f"Lineplot for {SITENAME} - from midnight",
        ),
    )


@app.route("/lineplot_last24hours")
def lineplot_last24():
    return render_template(
        "gt2.html",
        plot=plt_scatter.plot(
            slice_s1(start="24 hours ago"),
            title=f"Lineplot for {SITENAME} - last 24 hours",
        ),
    )


@app.route("/heatmap_last30days")
def heatmap():
    return render_template(
        "gt2.html",
        plot=plt_heatmap.plot(
            slice_s1(start="30 days ago"),
            title=f"Download avg (Mbit/s) for {SITENAME} - last 30 days",
        ),
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
