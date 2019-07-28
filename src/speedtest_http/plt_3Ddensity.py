# -*- coding: utf-8 -*-

"""
TODO
"""

import json
import logging

import pandas as pd
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
    # prepare bins
    try:
        bin_max = int(df.Download.max()) + 1
    except ValueError:  # the case of only Nan
        bin_max = 0
    bin_range = range(1, bin_max + 1)

    # prepare grouping by a given time unit
    df["Time"] = [
        ts.replace(hour=0, minute=0, second=0, microsecond=0)
        for ts in df["tslocal"]
    ]

    # append bins for Download values
    df["Speed"] = pd.cut(
        x=df.Download, bins=bin_range, labels=range(1, bin_max)
    )

    # append a density column to aggregate
    df["Density"] = 1

    # cleanup before grouping
    d3 = df.drop(["Download", "Upload"], axis=1)

    # GroupBy with dimensions time, speed, density
    g3 = d3.groupby(by=[d3.Time, d3.Speed], as_index=False).sum()

    # make the graph
    fig = go.Figure()

    fig.add_trace(
        go.Scatter3d(
            x=df.Density,
            y=df.Time,
            z=df.Speed,
            name="rug",
            mode="markers",
            marker=dict(size=1),
        )
    )

    fig.add_trace(
        go.Scatter3d(
            x=g3.Density,
            y=g3.Time,
            z=g3.Speed,
            name="density",
            mode="markers",
            marker=dict(
                size=2, color=1 / g3.Density, colorscale="viridis", opacity=0.7
            ),
        )
    )

    # TODO Graph width/ height: plotly only accepts px values so far,
    #      so set these with care and watch out for API improvements.
    fig.layout = dict(
        title_text=title,
        yaxis=go.layout.YAxis(type="date"),
        scene_camera_eye=dict(x=1, y=3, z=-0.1),
        scene=dict(
            xaxis_title="density (no unit)",
            yaxis_title="time",
            zaxis_title="speed (Mbit/s)",
        ),
        width=1280, height=720
    )

    return json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
