# -*- coding: utf-8 -*-

"""Provides functions to time-slice data frames produced by
module `reader`.

TODO tested manually, but still needs quality assurance in the form of
     automated unit tests.
"""
import logging

from datetime import datetime as dt
from datetime import timedelta
from pytz import timezone as tz

from localpy.ng import reader

__author__ = "Tobias Frei"
__copyright__ = "Tobias Frei"
__license__ = "gpl2"

_logger = logging.getLogger(__name__)


def _slice(df, start, end):
    """Slice input df using start and end."""

    _logger.debug(f"{start} is lower bound of slice")
    _logger.debug(f"{end} is upper bound of slice")

    mask = df.set_index("Timestamp")

    # Find index values for slicing.
    lower = mask.index.searchsorted(start)
    upper = mask.index.searchsorted(end)

    # Slice according to values.
    if start:
        if end:
            df = mask.iloc[lower:upper]
        else:
            df = mask.iloc[lower:]
    else:
        if end:
            df = mask.iloc[:upper]
        else:
            df = mask

    _logger.debug(f"{df.index.min()} is min index in DataFrame")
    _logger.debug(f"{df.index.max()} is max index in DataFrame")

    # print(df)

    return df


def _naive_to_utc(time_in, localzone):
    """A simple converter, local timezone to UTC."""
    return tz(localzone).localize(time_in).astimezone(tz("UTC"))


def get_by_timestamps(infile, start=None, end=None, myzone="UTC"):
    """Read infile into a DataFrame and return a time slice, defined by
    start (timestamp) and end (timestamp).
        Args:
            infile      csv, as produced by `speedtest-cli --csv`
            start_time  timezone-agnostic start value
            end_time    timezone-agnostic end value

            myzone      local timezone as string

            Type of start_time and end_time MUST be `datetime.datetime`.
        Return:
            DataFrame, start_timestamp (UTC), end_timestamp (UTC)
    """
    df = reader.speedtest_read(infile, myzone=myzone, agnostic=True)

    if start:
        start = _naive_to_utc(start, myzone)

    if end:
        end = _naive_to_utc(end, myzone)

    return _slice(df, start, end), start, end


def get_by_name(infile, name=None, myzone="UTC"):
    """Read infile into a DataFrame and return a time slice, defined by
    a time-frame with an intuitive name.
        Args:
            infile      csv, as produced by `speedtest-cli --csv`
            name        `last24hours`       | `last7days`    | `last30days`  |
                        `from_midnight`     | `from_sunday`  | `from_monday` |
                        `from_1st_of_month` | `from_jan_1st` | `all`

            If name is `None` all valid names are returned in a `list`.

            myzone      local timezone as string
        Return:
            DataFrame, start_timestamp (UTC), end_timestamp (UTC)
    """
    if name is None:
        return [
            "last24hours",
            "last7days",
            "last30days",
            "from_midnight",
            "from_sunday",
            "from_monday",
            "from_1st_of_month",
            "from_jan_1st",
            "all",
        ]
    else:
        # helper variables
        now = dt.now()
        weekday = dt.now().isoweekday()
        last_midnight = dt.combine(dt.now(), dt.min.time())

        if name == "last24hours":
            start = now - timedelta(days=1)
        elif name == "last7days":
            start = now - timedelta(days=7)
        elif name == "last30days":
            start = now - timedelta(days=30)
        elif name == "from_midnight":
            start = last_midnight
        elif name == "from_sunday":
            delta = 7 if weekday == 0 else weekday
            start = last_midnight - timedelta(days=delta)
        elif name == "from_monday":
            delta = 7 if weekday == 0 else weekday
            delta -= 1  # reduce by 1
            start = last_midnight - timedelta(days=delta)
        elif name == "from_1st_of_month":
            start = last_midnight.replace(day=1)
        elif name == "from_jan_1st":
            start = last_midnight.replace(day=1, month=1)
        else:
            start = None

        # In all our cases so far end is `None` (i.e. the present).
        end = now

        return get_by_timestamps(infile, start=start, end=end, myzone=myzone)
