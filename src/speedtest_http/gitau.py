# -*- coding: utf-8 -*-

"""
Inspired by Yvonne Gitau (https://github.com/yvonnegitau/flask-Dashboard)
"""

import json

import numpy as np
import pandas as pd
import plotly
import plotly.graph_objs as go


def plot(feature):
    """Yvonne Gitau's example
    Args:
        feature     what we got from AJAX
    """
    if feature == "Bar":
        N = 40
        x = np.linspace(0, 1, N)
        y = np.random.randn(N)
        df = pd.DataFrame({"x": x, "y": y})  # creating a sample dataframe

        data = [
            go.Bar(
                x=df["x"], y=df["y"]
            )  # assign x as the dataframe column 'x'
        ]

    else:
        # create a trace
        N = 10**6
        rand_x = np.random.randn(N)
        rand_y = np.random.randn(N)

        data = [go.Scattergl(x=rand_x, y=rand_y, mode="markers")]

    return json.dumps(data, cls=plotly.utils.PlotlyJSONEncoder)
