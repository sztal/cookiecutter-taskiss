"""Command-line interface utilities."""
# pylint: disable=W0613
import json
from collections import Iterable, Sequence, Mapping, defaultdict
from types import GeneratorType
from ast import literal_eval
import click
from {{ cookiecutter.repo_name }}.config import cfg, MODE
from {{ cookiecutter.repo_name }}.utils import safe_print
from {{ cookiecutter.repo_name }}.utils.serializers import UniversalJSONEncoder
from .exceptions import MalformedArgumentError, RepeatedArgumentError


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

def eager_callback(callback):
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
    def callback_wrapper(ctx, param, value, *args, **kwds):
        """Wrapped callback."""
        if not value or ctx.resilient_parsing:
            return
        callback(*args, **kwds)
        ctx.exit()
    return callback_wrapper

def to_console(obj, unique=False, processor=None, **kwds):
    """Print object to the console.

    Parameters
    ----------
    obj : any
        String and non-terables are printed as is.
        Other iterables are iterated and printed.
        Iterables within iterables are printed as is.
    unique : bool
        Should duplicated objects be shown only once.
    processor : func or None
        Optional processing function to call on each object.
    **kwds :
        Keyword arguments passed to the processor function.
    """
    if isinstance(obj, str) or not isinstance(obj, (Sequence, GeneratorType)):
        obj = [obj]
    if unique:
        show_unique(obj)
    for o in obj:
        if processor:
            o = processor(o, **kwds)
        pprint(o)

def parse_args(*args, parser=None, repeated=False):
    """Parse command-line arguments.

    Parameters
    ----------
    *args :
        Sequence of arguments provided as string of form 'key=value'.
    parser : { None, 'eval', 'json' }
        If `None` the values remain ordinary strings.
        If `eval` then :py:func:`ast.literal_eval` is called on values.
        If `json` then :py:meth:`json.loads` is used to parse the values.
    repeated : bool
        Should repeated arguments be allowed.
        Note that in this case all keys' values are represented as lists.
    """
    kwds = defaultdict(list) if repeated else {}
    for arg in args:
        try:
            key, value = arg.split("=")
            key = key.strip()
            value = value.strip()
        except ValueError:
            raise MalformedArgumentError.from_arg(arg)
        try:
            if parser == 'json':
                value = json.loads(value)
            elif parser == 'eval':
                value = literal_eval(value)
        except (ValueError, TypeError):
            raise MalformedArgumentError.from_arg(arg)
        if repeated:
            kwds[key].append(value)
        else:
            if key in kwds:
                raise RepeatedArgumentError.from_arg(key, [ kwds[key], value ])
            kwds[key] = value
    return dict(kwds)

def do_dry_run(dry, *args):
    """Dry run."""
    if dry:
        for arg in args:
            to_console(arg)
        ctx = click.get_current_context()
        ctx.exit()
