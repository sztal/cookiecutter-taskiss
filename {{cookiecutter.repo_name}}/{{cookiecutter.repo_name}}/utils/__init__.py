"""Miscellaneous and general purpose utilities."""
import re
from importlib import import_module
from pkgutil import walk_packages
from click import echo

_rx_pp = re.compile(r"^[\w_.:]+$", re.ASCII)

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

def import_python(path, package=None):
    """Get python module or object.

    Parameters
    ----------
    path : str
        Fully-qualified python path, i.e. `package.module:object`.
    package : str or None
        Package name to use as an anchor if `path` is relative.
    """
    parts = path.split(':')
    if len(parts) > 2:
        msg = f"Not a correct path ('{path}' has more than one object qualifier)"
        raise ValueError(msg)
    elif len(parts) == 2:
        module_path, obj = parts
    else:
        module_path, obj = path, None
    module = import_module(module_path, package=package)
    if obj:
        return getattr(module, obj)
    return module

def is_python_path(path):
    """Check if a string is a valid python path.

    Parameters
    ----------
    path : str
        String.
    """
    m = _rx_pp.match(path)
    if not m or path.count(':') > 1:
        return False
    return True

def iter_objects(path='.', mod_predicate=None, obj_predicate=None, skip_private=True,
                 skip_modules=('test', 'tests', 'doc', 'docs')):
    """Import all objects with optional predicate based filtering.

    Parameters
    ----------
    path : str
        Proper python module path.
    mod_predicate : callable or None
        Predicate function for filtering modules.
    obj_predictae : callable or None
        Predicate function for filtering objects.
    skip_private : bool
        Should private objects (starting with '_') be omitted.
    skip_modules : list of str
        List of module names to skip.
    """
    _path = path.replace('.', '', 1) if path.startswith('.') else path
    for _, name, _ in walk_packages(path):
        if not name.startswith(_path):
            continue
        path_parts = name.split('.')
        for p in path_parts:
            if (skip_private and p.startswith('_')) \
            or (skip_modules and p in skip_modules):
                continue
        if mod_predicate and not mod_predicate(name):
            continue
        module = import_python(name)
        for _, obj in module.__dict__.items():
            if obj_predicate and obj_predicate(obj):
                yield obj
