# -*- coding: utf-8 -*-

"""Please see function `layout`.
"""

import logging

import dash_core_components as dcc
import dash_html_components as html

import plotly.graph_objs as go

from localpy.ng import slicer

__author__ = "Tobias Frei"
__copyright__ = "Tobias Frei"
__license__ = "gpl2"

_logger = logging.getLogger(__name__)


def layout(INFILE, TZ, SITENAME, shorthand=None):
    """Plot lines for Download, markers for upload.
    Time-frames are configurable via shorthands (e.g. `last24hours`).
    Upon success a `dash` html div is returned to be rendered.
    """
    df, _, _ = slicer.get_by_name(INFILE, name=shorthand, myzone=TZ)

    return html.Div(
        # className="col-lg-10",
        dcc.Graph(
            id="fig1",
            figure={
                "data": [
                    go.Scatter(
                        x=df["agnostic_t"],
                        y=df["Download"],
                        mode="lines",
                        name="Download"
                    ),
                    go.Scatter(
                        x=df["agnostic_t"],
                        y=df["Upload"],
                        mode="markers",
                        name="Upload"
                    ),
                ],
                "layout": go.Layout(
                    title=f"Lineplot for {SITENAME}",
                    xaxis={"title": shorthand},
                    yaxis={"title": "speed (Mbit/s)"},
                    # legend={"x": 0, "y": 1},
                ),
            },
            animate=False,
            style={"height": "70vh", "width": "95vw"},
        ),
        style={"padding-top": "30px"},
    )
