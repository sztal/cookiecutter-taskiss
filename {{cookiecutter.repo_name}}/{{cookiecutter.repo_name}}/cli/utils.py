"""Command-line interface utilities."""
# pylint: disable=W0613
import json
from collections import Iterable, Sequence, Mapping, defaultdict
from types import GeneratorType
from ast import literal_eval
from {{ cookiecutter.repo_name }}.config import cfg, MODE
from {{ cookiecutter.repo_name }}.utils import safe_print
from {{ cookiecutter.repo_name }}.cli.exceptions import MalformedArgumentError, RepeatedArgumentError
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

def show_unique(iterator):
    """Show unique values in an iterator."""
    shown = []
    for item in iterator:
        if item in shown:
            continue
        shown.append(item)
        pprint(item)

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

def to_console(obj, unique=False):
    """Print object to the console.

    Parameters
    ----------
    obj : any
        String and non-terables are printed as is.
        Other iterables are iterated and printed.
        Iterables within iterables are printed as is.
    unique : bool
        Should duplicated objects be shown only once.
    """
    if isinstance(obj, str) or not isinstance(obj, (Sequence, GeneratorType)):
        obj = [obj]
    if unique:
        show_unique(obj)
    for o in obj:
        pprint(o)

def parse_args(*args, eval_args=False, repeated=False):
    """Parse command-line arguments.

    Parameters
    ----------
    *args :
        Sequence of arguments provided as string of form 'key=value'.
    eval_args : bool
        If `eval_args=True` then value are first evaluated as literal python
        code using safe evaluation implemented in
        :py:function:`ast.literal_eval`.
    repeated : bool
        Should repeated arguments be allowed.
        Note that in this case all keys' values are represented as lists.
        In fact, a `defaultdict(list)` is returned.
    """
    kwds = defaultdict(list) if repeated else {}
    for arg in args:
        try:
            key, value = arg.split("=")
        except ValueError:
            raise MalformedArgumentError.from_arg(arg)
        if eval_args:
            try:
                value = literal_eval(value)
            except (ValueError, TypeError):
                raise MalformedArgumentError.from_arg(arg)
        if repeated:
            kwds[key].append(value)
        else:
            if key in kwds:
                raise RepeatedArgumentError.from_arg(key, [ kwds[key], value ])
            kwds[key] = value
    return kwds
