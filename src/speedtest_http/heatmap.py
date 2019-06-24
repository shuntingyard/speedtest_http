# -*- coding: utf-8 -*-

"""Please see function `layout`.
"""

import logging

import dash_core_components as dcc
import dash_html_components as html
import numpy as np
import pandas as pd
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


def layout(INFILE, TZ, SITENAME, start=None, end=None):
    """Plot a heatmap TBD...TBD!

    Time-frames are configurable via shorthands (e.g. `last24hours`).
    Upon success a `dash` html div is returned to be rendered.
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

    # customize details
    hovertext = []
    for hour in corr.values.tolist():
        hovertext.append([])
        for hval in hour:
            hovertext[-1].append(
                "{}".format("no values at this time")
                if pd.isna(hval)
                else f"DL speed: {round(hval, 2)} Mbit/s"
            )

    return html.Div(
        # className="col-lg-10",
        dcc.Graph(
            id="fig1",
            figure={
                "data": [
                    go.Heatmap(
                        x=corr.columns,
                        y=corr.index,
                        z=corr.values,
                        text=hovertext,
                        hoverinfo=("text"),
                    )
                ],
                "layout": go.Layout(
                    title=f"Download avg (Mbit/s) for {SITENAME}",
                    xaxis=dict(title=start, showgrid=False),
                    yaxis=dict(showgrid=False, tick0=0),
                ),
            },
            animate=False,
            style={"height": "85vh", "width": "95vw"},
        ),
        style={"padding-top": "15px"},
    )
