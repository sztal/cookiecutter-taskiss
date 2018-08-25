"""Miscellaneous and general purpose utilities."""

from click import echo

def safe_print(x, **kwds):
    """Fault-safe print function.

    Parameters
    ----------
    x : any
        An object dumpable to str.
    **kwds :
        Other arguments passed to `click.echo`.
    """
    try:
        echo(x, **kwds)
    except UnicodeEncodeError:
        x = str(x).encode('utf-8', 'replace')
        echo(x, **kwds)
