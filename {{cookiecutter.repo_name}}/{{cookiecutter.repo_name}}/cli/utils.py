"""Command-line interface utilities."""
# pylint: disable=W0613
import json
from collections import Iterable, Mapping
from ast import literal_eval
from {{ cookiecutter.repo_name }}.config import cfg, MODE
from {{ cookiecutter.repo_name }}.utils import safe_print
from {{ cookiecutter.repo_name }}.cli.exceptions import MalformedArgumentError
from {{ cookiecutter.repo_name }}.utils.serializers import UniversalJSONEncoder


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
        safe_print(json.dumps(obj, sort_keys=True, indent=indent, cls=UniversalJSONEncoder))
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

def parse_args(*args, eval_args=False):
    """Parse command-line arguments.

    Parameters
    ----------
    *args :
        Sequence of arguments provided as string of form 'key=value'.
    eval_args : bool
        If `eval_args=True` then value are first evaluated as literal python
        code using safe evaluation implemented in
        :py:function:`ast.literal_eval`.
    """
    kwds = {}
    for arg in args:
        try:
            key, value = arg.split("=")
        except ValueError:
            raise MalformedArgumentError(arg)
        if eval_args:
            try:
                value = literal_eval(value)
            except (ValueError, TypeError):
                raise MalformedArgumentError(arg)
        kwds[key] = value
    return kwds
