# -*- coding: utf-8 -*-

"""Please see function `layout`.
"""

import json
import logging

import plotly
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
    Upon success a plotly-JSON-encoded graph is returned.
    """
    if start:
        df = read_by_ts(INFILE, start=start)
    else:
        df = read_by_mnemonic(INFILE, mnemonic=mnemonic)

    graph = dict(
        data=[
            go.Scatter(
                x=df["tslocal"],
                y=df["Download"],
                mode="lines",
                connectgaps=False,
                name="Download"
            ),
            go.Scatter(
                x=df["tslocal"],
                y=df["Upload"],
                mode="markers",
                name="Upload"
            ),
        ],
        # TODO Graph width/ height: plotly only accepts px values so far,
        #      so set these with care and watch out for API improvements.
        layout=go.Layout(
            title=f"Lineplot for {SITENAME}",
            xaxis={"title": start if start else mnemonic},
            yaxis={"title": "speed (Mbit/s)"},
            # legend={"x": 0, "y": 1},
            ),
        )

    return json.dumps(graph, cls=plotly.utils.PlotlyJSONEncoder)
