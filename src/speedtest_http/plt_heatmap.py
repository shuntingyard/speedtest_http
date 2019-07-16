# -*- coding: utf-8 -*-

"""
To be done
"""

import json
import logging

import numpy as np
import pandas as pd
import plotly
import plotly.graph_objs as go

from speedtest_reader import read_by_ts
from speedtest_reader import reader

# decorate
read_by_ts = reader.bit_to_Mbit(read_by_ts)
read_by_ts = (reader.append_tslocal())(read_by_ts)

__author__ = "Tobias Frei"
__copyright__ = "Tobias Frei"
__license__ = "mit"

_logger = logging.getLogger(__name__)


def plot(INFILE, TZ, SITENAME, start=None, end=None):
    """Plot a heatmap TBD...TBD!

    Time-frames are configurable via shorthands (e.g. `last24hours`).
    Upon success a plotly-JSON-encoded graph is returned.
    """
    df = read_by_ts(INFILE, start=start)

    # Data preparation

    # First add hour and date columns.
    df["hour"] = [ts.strftime("%H:00") for ts in df["tslocal"]]
    df["date"] = [ts.strftime("%m-%d %a") for ts in df["tslocal"]]
    # FIXME these are now back to the UTC bug. So we need decorators
    #      (agnostic-t) in the near future.

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
                "{}".format("no values at this time")
                if pd.isna(hval)
                else f"DL speed: {round(hval, 2)} Mbit/s"
            )

    graph = dict(
        data=[
            go.Heatmap(
                x=corr.columns,
                y=corr.index,
                z=corr.values,
                text=hovertext,
                hoverinfo=("text"),
            )
        ],
        # TODO Graph width/ height: plotly only accepts px values so far,
        #      so set these with care and watch out for API improvements.
        layout=go.Layout(
            title=f"Download avg (Mbit/s) for {SITENAME}",
            xaxis=dict(title=start, showgrid=False, automargin=True),
            yaxis=dict(showgrid=False, tick0=0),
            height=600
        ),
    )

    return json.dumps(graph, cls=plotly.utils.PlotlyJSONEncoder)
