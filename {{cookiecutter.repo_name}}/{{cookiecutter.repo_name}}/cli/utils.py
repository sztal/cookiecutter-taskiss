"""Command-line interface utilities."""
# pylint: disable=W0613
import json
from collections import Iterable, Mapping
from {{ cookiecutter.repo_name }}.config import cfg, MODE
from {{ cookiecutter.repo_name }}.utils import safe_print


def pprint(obj, indent=None):
    """Pretty print json-like objects.

    Parameters
    ----------
    obj : any
        Some object.
    indent : int or None
        Indentation length.
        If `None` then config value is used.
    """
    if not indent:
        indent = cfg.getint(MODE, 'pp_indent', fallback=2)
    if isinstance(obj, (list, tuple, Mapping)):
        safe_print(json.dumps(obj, sort_keys=True, indent=indent))
    else:
        safe_print(obj)

def eager_callback(callback, *args, **kwds):
    """Warpper for executing callbacks of eager options.

    Parameters
    ----------
    ctx : :py:class:`click.Context`
        Context object.
    value : any
        Value.
    *args :
        Positional arguments passed to the callback.
    **kwds :
        Keyword arguments passed to the callback.
    """
    def callback_wrapper(ctx, param, value):
        """Wrapped callback."""
        if not value or ctx.resilient_parsing:
            return
        callback(*args, **kwds)
        ctx.exit()
    return callback_wrapper

def to_console(obj):
    """Print object to the console.

    Parameters
    ----------
    obj : any
        String and non-terables are printed as is.
        Other iterables are iterated and printed.
        Iterables within iterables are printed as is.
    """
    if isinstance(obj, str) or isinstance(obj, Mapping) \
    or not isinstance(obj, Iterable):
        obj = [obj]
    for o in obj:
        pprint(o)
