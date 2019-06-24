# -*- coding: utf-8 -*-

"""
A router to a couple of dash plots.
"""

import dash
import dash_core_components as dcc
import dash_html_components as html

from dash.dependencies import Input
from dash.dependencies import Output

# production plots
from speedtest_http import heatmap
from speedtest_http import lineplot

# environmental
from speedtest_http import INFILE
from speedtest_http import SITENAME
from speedtest_http import srv
from speedtest_http import TZ

__author__ = "Tobias Frei"
__copyright__ = "Tobias Frei"
__license__ = "mit"

# Define the hosted dash app.
_external_stylesheets = ["https://codepen.io/chriddyp/pen/bWLwgP.css"]
app = dash.Dash(
    __name__,
    external_stylesheets=_external_stylesheets,
    meta_tags=[
        {"name": "viewport", "content": "width=device-width, initial-scale=1"}
    ],
    server=srv,
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

    srv.logger.debug(f"Serving route: {pathname}")

    if pathname == "/data/lineplot_today":
        return lineplot.layout(INFILE, TZ, SITENAME, mnemonic="from_midnight")
    elif pathname == "/data/lineplot_last24hours":
        return lineplot.layout(INFILE, TZ, SITENAME, start="24 hours ago")
    elif pathname == "/data/heatmap_last30days":
        return heatmap.layout(INFILE, TZ, SITENAME, start="30 days ago")

    else:
        if pathname:
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
