# -*- coding: utf-8 -*-
"""
Use range selector buttons to inspect data in a window of variable size
(according to selections).
"""

import json
import logging

from datetime import datetime

import plotly
import plotly.graph_objs as go

from speedtest_reader import util

__author__ = "Tobias Frei"
__copyright__ = "Tobias Frei"
__license__ = "mit"

logger = logging.getLogger(__name__)


@util.stopwatch
def plot(df, title):
    """
    Upon success a plotly-JSON-encoded graph is returned.
    """
    graph = dict(
        data=[
            go.Scattergl(
                x=df.tslocal,
                y=df.Download,
                mode="lines",
                name="Download",
                connectgaps=False,
            ),
            go.Scattergl(
                x=df.tslocal, y=df.Upload, mode="markers", name="Upload"
            ),
        ],
        # TODO Graph width/ height: plotly only accepts px values so far,
        #      so set these with care and watch out for API improvements.
        layout=go.Layout(
            title=f"{title}",
            xaxis=dict(
                rangeselector=dict(
                    buttons=list(
                        [
                            dict(
                                count=1,
                                label="today",
                                step="day",
                                stepmode="todate",
                            ),
                            dict(
                                count=1,
                                label="24h",
                                step="day",
                                stepmode="backward",
                            ),
                            dict(
                                count=2,
                                label="48h",
                                step="day",
                                stepmode="backward",
                            ),
                            dict(
                                count=3,
                                label="3 days",
                                step="day",
                                stepmode="backward",
                            ),
                            dict(
                                count=4,
                                label="4d",
                                step="day",
                                stepmode="backward",
                            ),
                            dict(
                                count=5,
                                label="5d",
                                step="day",
                                stepmode="backward",
                            ),
                            dict(
                                count=6,
                                label="6d",
                                step="day",
                                stepmode="backward",
                            ),
                            dict(
                                count=7,
                                label="7d",
                                step="day",
                                stepmode="backward",
                            ),
                            dict(
                                count=30,
                                label="30d",
                                step="day",
                                stepmode="backward",
                            ),
                            dict(
                                count=datetime.today().isoweekday(),
                                label="this week",
                                step="day",
                                stepmode="todate",
                            ),
                        ]
                    )
                )
            ),
            yaxis=dict(title="speed (Mbit/s)"),
        ),
    )

    return json.dumps(graph, cls=plotly.utils.PlotlyJSONEncoder)
