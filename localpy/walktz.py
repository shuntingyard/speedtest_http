import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
from datetime import datetime as dt
import datetime
import pytz

tz_east = pytz.timezone("US/Eastern")

dt_utc = dt.utcnow()
dt_set = dt(2019, 3, 7, 13, 32)
dt_now = dt.now()
dt_aware_east = dt_utc.astimezone(tz_east)


def genFigData():
    figDataCombined = list()

    dateList1 = [
        dt_utc,
        dt_utc + datetime.timedelta(minutes=30),
        dt_utc + datetime.timedelta(minutes=60),
    ]
    dateList2 = [
        dt_set,
        dt_set + datetime.timedelta(minutes=31),
        dt_set + datetime.timedelta(minutes=61),
    ]
    dateList3 = [
        dt_now,
        dt_now + datetime.timedelta(minutes=32),
        dt_now + datetime.timedelta(minutes=62),
    ]
    dateList4 = [
        dt_aware_east,
        dt_aware_east + datetime.timedelta(minutes=33),
        dt_aware_east + datetime.timedelta(minutes=63),
    ]

    for i in range(0, 3):
        print(
            "var: dt_utc, date:{}, type:{}".format(
                dateList1[i], type(dateList1[i])
            )
        )
        print(
            "var: dt_set, date:{}, type:{}".format(
                dateList2[i], type(dateList2[i])
            )
        )
        print(
            "var: dt_now, date:{}, type:{}".format(
                dateList3[i], type(dateList3[i])
            )
        )
        print(
            "var: dt_aware_east, date:{}, type:{}".format(
                dateList4[i], type(dateList4[i])
            )
        )

    valList1 = [1, 2, 3]
    figData1 = go.Scatter(
        x=list(dateList1),
        y=list(valList1),
        name="dt.utcnow()",
        mode="lines+markers",
    )
    figData2 = go.Scatter(
        x=list(dateList2),
        y=list(valList1),
        name="dt(y,mo,d...)",
        mode="lines+markers",
    )
    figData3 = go.Scatter(
        x=list(dateList3),
        y=list(valList1),
        name="dt.now()",
        mode="lines+markers",
    )
    figData4 = go.Scatter(
        x=list(dateList4),
        y=list(valList1),
        name="dt_aware_east",
        mode="lines+markers",
    )

    figDataCombined.append(figData1)
    figDataCombined.append(figData2)
    figDataCombined.append(figData3)
    figDataCombined.append(figData4)

    figLayout = dict(
        title="timezone_test_graph: Eastern Time={}".format(dt.now()),
        xaxis=dict(rangeslider=dict(visible=True), type="date"),
    )
    fig1 = go.Figure(data=figDataCombined, layout=figLayout)
    return fig1


def layout():
    return html.Div(
        [
            # deg.ExtendableGraph(
            dcc.Graph(id="timezone_test_graph", figure=genFigData()),
            html.Div(
                [
                    html.P("dt_utc = {}".format(dt_utc)),
                    html.P("dt_set = {}".format(dt_set)),
                    html.P("dt_now = {}".format(dt_now)),
                    html.P("dt_aware_east = {}".format(dt_aware_east)),
                ]
            ),
        ]
    )
