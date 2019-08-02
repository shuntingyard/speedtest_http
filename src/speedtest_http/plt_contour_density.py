# -*- coding: utf-8 -*-
"""
Visualize download speed density data by counting values in (daily) bins
and showing the counter's positions in 3D.
"""

import json
import logging

import numpy as np
import pandas as pd
import plotly
import plotly.graph_objs as go

from speedtest_reader import util

__author__ = "Tobias Frei"
__copyright__ = "Tobias Frei"
__license__ = "mit"

logger = logging.getLogger(__name__)


@util.stopwatch
def plot(df, title, colorscale=None):
    """
    Upon success a plotly-JSON-encoded graph is returned.
    """
    # prepare bins
    try:
        bin_max = int(df.Download.max()) + 2
    except ValueError:  # the case of only Nan
        bin_max = 2

    # prepare grouping by a given time unit
    df["Time"] = [
        ts.replace(hour=0, minute=0, second=0, microsecond=0)
        for ts in df["tslocal"]
    ]

    # append bins for Download values
    df["Speed"] = pd.cut(
        x=df.Download,
        bins=range(bin_max),
        labels=range(bin_max - 1),
        right=False,
    )

    # append a density column to aggregate
    df["Density"] = 1

    # cleanup
    df = df.drop(["Download", "Upload"], axis=1)

    # summarize
    p3 = pd.pivot_table(
        df, index="Speed", columns="Time", values="Density", aggfunc=np.sum
    )
    print(p3)

    # make the graph
    data = [go.Contour(z=p3, line_smoothing=0, contours_coloring="heatmap", colorscale=colorscale)]

    layout = go.Layout(
        title=title,
        width=768,
        height=768,
        autosize=False,
        xaxis=dict(title="days (ordinal)", tick0=0, dtick=1, showticklabels=False),
        yaxis=dict(title="speed (Mbit/s)", showgrid=False),
    )

    fig = go.Figure(data=data, layout=layout)

    return json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
