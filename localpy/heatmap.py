# -*- coding: utf-8 -*-

"""Please see function `layout`.
"""

import logging

import dash_core_components as dcc
import dash_html_components as html
import numpy as np
import pandas as pd
import plotly.graph_objs as go

from localpy.ng import slicer

__author__ = "Tobias Frei"
__copyright__ = "Tobias Frei"
__license__ = "gpl2"

_logger = logging.getLogger(__name__)


def layout(ramdf, TZ, SITENAME, shorthand=None):
    """Plot a heatmap TBD...TBD!

    Time-frames are configurable via shorthands (e.g. `last24hours`).
    Upon success a `dash` html div is returned to be rendered.
    """
    df, _, _ = slicer.get_by_name(ramdf, name=shorthand, myzone=TZ)

    # Data preparation

    # First add hour and date columns.
    df["hour"] = [ts.strftime("%H:00") for ts in df["agnostic_t"]]
    df["date"] = [ts.strftime("%m-%d %a") for ts in df["agnostic_t"]]

    # Then use pandas' pivot table function.
    corr = pd.pivot_table(
        df, index="hour", columns="date", values="Download", aggfunc=np.mean
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
                    )
                ],
                "layout": go.Layout(
                    title=f"Download avg (Mbit/s) for {SITENAME}",
                    xaxis=dict(
                        title=shorthand,
                        showgrid=False
                    ),
                    yaxis=dict(
                        showgrid=False,
                        tick0=0,
                    ),
                ),
            },
            animate=False,
            style={"height": "85vh", "width": "95vw"},
        ),
        style={"padding-top": "15px"},
    )
