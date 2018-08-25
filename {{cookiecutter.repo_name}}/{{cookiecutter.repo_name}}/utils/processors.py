"""Serializer functions for transfering data from and to the ODM."""

from datetime import datetime, date
import dateparser


def date_from_string(dt, fmt, preprocessor=None, **kwds):
    """Convert string to :py:class:`datetime.datetime` object.

    Parameters
    ----------
    dt : str
        Date string.
    frm : str
        Date formatting string.
    preprocessor : func
        Optional preprocessing function.
        Useful for normalizing date strings to conform to one format string.
    **kwds :
        Arguments passed to `preprocessor`.
    """
    if isinstance(dt, datetime):
        return dt
    if isinstance(dt, date):
        return datetime(*dt.timetuple()[:6])
    if preprocessor:
        dt = preprocessor(dt, **kwds)
    return datetime.strptime(dt, fmt)

def parse_date(dt, preprocessor=None, **kwds):
    """Parse date string flexibly using `dateutil` module.

    Parameters
    ----------
    dt : str
        Date string.
    preprocessor : func
        Optional preprocessing function.
        Useful for normalizing date strings to conform to one format string.
    **kwds :
        Arguments passed to `preprocessor`.
    """
    if isinstance(dt, datetime):
        return dt
    if isinstance(dt, date):
        return datetime(*dt.timetuple()[:6])
    if preprocessor:
        dt = preprocessor(dt, **kwds)
    return dateparser.parse(dt)

def parse_bool(x):
    """Parse boolean string."""
    if isinstance(x, bool):
        return x
    x = x.lower()
    if x in ('true', 'yes'):
        return True
    if x in ('false', 'no'):
        return False
    raise ValueError("Value '{}' can not be interpreted as boolean".format(x))
