# -*- coding: utf-8 -*-
"""
Give an overview by aggregating download speed value data (per hour) and
arranging results in a heat map.
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
def plot(df, title):
    """
    Upon success a plotly-JSON-encoded graph is returned.
    """
    # Data preparation

    # First add hour and date columns.
    df["hour"] = [ts.strftime("%H:00") for ts in df["tslocal"]]
    df["date"] = [ts.strftime("%m-%d %a") for ts in df["tslocal"]]

    # Then use pandas' pivot table function.
    corr = pd.pivot_table(
        df, index="hour", columns="date", values="Download", aggfunc=np.mean
    )

    # customize hovertext for heat spots
    hovertext = []
    for hour in corr.values.tolist():
        hovertext.append([])
        for hval in hour:
            hovertext[-1].append(
                "{}".format("no value at this time")
                if pd.isna(hval)
                else f"{round(hval, 2)} Mbit/s"
            )

    # make the graph
    data = [
        go.Heatmap(
            x=corr.columns,
            y=corr.index,
            z=corr.values,
            # text=hovertext,
            # hoverinfo=("text"),
            colorscale="blues",
            zsmooth="best",
        )
    ]

    layout = go.Layout(
        title=title,
        width=768,
        height=768,
        autosize=False,
        xaxis=dict(showgrid=False, automargin=True),
        yaxis=dict(showgrid=False, tick0=0, dtick=1),
    )

    fig = go.Figure(data=data, layout=layout)

    return json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
