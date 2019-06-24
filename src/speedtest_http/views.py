# -*- coding: utf-8 -*-

"""
The V-module (from MVC)...
"""

from flask import render_template

from speedtest_http import SITENAME
from speedtest_http import srv

__author__ = "Tobias Frei"
__copyright__ = "Tobias Frei"
__license__ = "mit"


@srv.route("/")
def _index():
    return render_template("index.html", sitename=SITENAME)


@srv.errorhandler(404)
def _http404_e(e):
    return render_template("404.html"), 404

# no routes to dash so far...
