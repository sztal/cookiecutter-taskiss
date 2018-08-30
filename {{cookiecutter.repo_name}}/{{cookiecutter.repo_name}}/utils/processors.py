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

def parse_bool(x, true=('true', 'yes', '1', 'on'), add_true=(),
               false=('false', 'no', '0', 'off'), add_false=()):
    """Parse boolean string.

    Parameters
    ----------
    x : bool or str
        Boolean value as `bool` or `str`.
    true : list of str
        List of accepted string representations of `True` value.
    add_true  : list of str
        Optional list to of `True` representations to append to the default list.
    false : list of str
        List of accepted string representations of `False` value.
    add_false : list of str
        Optional list of `False` representations to append to the default list.

    Notes
    -----
    `true` and `false` should always consist of only lowercase strings,
    as all comparisons are done after lowercasing `x`.

    Raises
    ------
    ValueError
        If `x` is not `bool` and not contained either in `true` or `false`.
    """
    if isinstance(x, bool):
        return x
    x = x.lower()
    if add_true:
        true = (*true, *add_true)
    if add_false:
        false = (*false, *add_false)
    if x in true:
        return True
    if x in false:
        return False
    raise ValueError("Value '{}' can not be interpreted as boolean".format(x))
