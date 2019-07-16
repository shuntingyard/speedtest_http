import functools
import time

import pandas as pd
import tzlocal

from matplotlib import dates as mdates
from pytz import timezone

from speedtest_reader import read_by_ts

# test settings
pd.options.display.max_rows = 7


def stopwatch(fn):
    """Measure how much time a function takes."""
    @functools.wraps(fn)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = fn(*args, **kwargs)
        end = time.perf_counter()
        elapsed = end - start
        print(f"Finished {fn.__name__!r} in {elapsed:.4f} secs")
        return result

    return wrapper


def to_Mbit(fn):
    """Convert bit to Mbit in upload and download columns."""
    @functools.wraps(fn)
    def wrapper(*args, **kwargs):

        df = kwargs["df"]
        df["Download"] = [f / 10 ** 6 for f in df["Download"]]
        df["Upload"] = [f / 10 ** 6 for f in df["Upload"]]
        return fn(*args, **kwargs)

    return wrapper


# --- decorators for speedtest_reader
def mpldate(colname="mpldate"):
    """Append timestamp column suitable for matplotlib (matplotlib.dates)."""
    def decorator(fn):
        @functools.wraps(fn)
        def wrapper(*args, **kwargs):

            df = kwargs["df"]
            df[colname] = [mdates.date2num(ts) for ts in df.index]
            return fn(*args, **kwargs)

        return wrapper

    return decorator


def tslocal(colname="tslocal"):
    """Append localized timestamp column - suitable for plotly, dash etc."""
    def decorator(fn):
        @functools.wraps(fn)
        def wrapper(*args, **kwargs):

            df = kwargs["df"]
            # Requires pandas >= 0.15.0 to get rid of tz.
            zone = kwargs["tz_slicer"]
            if zone:
                df[colname] = [
                    ts.astimezone(timezone(zone)).tz_localize(None)
                    for ts in df.index
                ]
            else:
                df[colname] = [
                    ts.astimezone(tzlocal.get_localzone()).tz_localize(None)
                    for ts in df.index
                ]
            return fn(*args, **kwargs)

        return wrapper

    return decorator
# --- end for speedtest_reader


# What the API call looks like
print(read_by_ts("/data/speedtest.csv", start="yesterday"))
