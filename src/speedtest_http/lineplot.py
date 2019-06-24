# -*- coding: utf-8 -*-

"""Please see function `layout`.
"""

import logging

import dash_core_components as dcc
import dash_html_components as html

import plotly.graph_objs as go

from speedtest_reader import read_by_mnemonic
from speedtest_reader import read_by_ts
from speedtest_reader import reader

# decorate
read_by_mnemonic = reader.bit_to_Mbit(read_by_mnemonic)
read_by_mnemonic = (reader.append_tslocal())(read_by_mnemonic)
read_by_ts = reader.bit_to_Mbit(read_by_ts)
read_by_ts = (reader.append_tslocal())(read_by_ts)

__author__ = "Tobias Frei"
__copyright__ = "Tobias Frei"
__license__ = "mit"

_logger = logging.getLogger(__name__)


def layout(INFILE, TZ, SITENAME, start=None, mnemonic=None):
    """Plot lines for Download, markers for upload.
    Time-frames are configurable via shorthands (e.g. `last24hours`).
    Upon success a `dash` html div is returned to be rendered.
    """
    if start:
        df = read_by_ts(INFILE, start=start)
    else:
        df = read_by_mnemonic(INFILE, mnemonic=mnemonic)

    return html.Div(
        dcc.Graph(
            id="fig1",
            figure={
                "data": [
                    go.Scatter(
                        x=df["tslocal"],
                        y=df["Download"],
                        mode="lines",
                        name="Download"
                    ),
                    go.Scatter(
                        x=df["tslocal"],
                        y=df["Upload"],
                        mode="markers",
                        name="Upload"
                    ),
                ],
                "layout": go.Layout(
                    title=f"Lineplot for {SITENAME}",
                    xaxis={"title": start if start else mnemonic},
                    yaxis={"title": "speed (Mbit/s)"},
                    # legend={"x": 0, "y": 1},
                ),
            },
            animate=False,
            style={"height": "70vh", "width": "95vw"},
        ),
        style={"padding-top": "30px"},
    )
