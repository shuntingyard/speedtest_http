# -*- coding: utf-8 -*-

"""Parse csv file produced by 'speedtest-cli' into pandas data frame.
"""

import matplotlib.dates as mdates
import pandas as pd

from pytz import timezone as tz

__author__ = "Tobias Frei"
__copyright__ = "Tobias Frei"
__license__ = "gpl2"


def speedtest_read(filename, myzone=None, mpl_ts=False, agnostic=False):
    """Read speedtest.csv file into pandas DataFrame.
        Args:
            filename    csv, as produced by `speedtest-cli --csv`
            myzone      optional timezone to localize `Timestamp`
            mpl_ts      Add matplotlib-friendly timestamp (col. `mtimestamp`).
            agnostic    Add timezone-agnostic timestamp (col. `agnostic_t`) -
                        makes no sense without `myzone` set!
        Return:
            DataFrame
    """
    with open(filename, "r") as infile:
        df = pd.read_csv(
            infile,
            engine="c",
            usecols=["Timestamp", "Download", "Upload"],
            converters={
                "Timestamp": lambda t: pd.to_datetime(t, utc=True),
                "Download": lambda d: float(d) / (1000000),
                "Upload": lambda u: float(u) / (1000000),
            },
        )

        # Localize `Timestamp`.
        if myzone:
            df["Timestamp"] = [
                ts.astimezone(tz(myzone)) for ts in df["Timestamp"]
            ]

        # Add matplotlib-friendly timestamp.
        if mpl_ts:
            df["mtimestamp"] = [mdates.date2num(ts) for ts in df["Timestamp"]]

        # Add timezone-agnostic timestamp
        if agnostic:
            df["agnostic_t"] = [
                ts.replace(tzinfo=None) for ts in df["Timestamp"]
            ]
        return df
