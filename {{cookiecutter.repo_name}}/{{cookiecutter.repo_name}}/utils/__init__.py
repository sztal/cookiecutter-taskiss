"""Miscellaneous and general purpose utilities."""
import re
from importlib import import_module
from pkgutil import walk_packages
from click import echo
from {{ cookiecutter.repo_name }}.exceptions import AmbiguousMatchError

_rx_pp = re.compile(r"^[\w_.:]+$", re.ASCII)

def safe_print(x, nl=True, **kwds):
    """Fault-safe print function.

    Parameters
    ----------
    x : any
        An object dumpable to str.
    nl : bool
        Should new line be printed after the content.
    **kwds :
        Other arguments passed to `click.echo`.
    """
    try:
        echo(x, nl=nl, **kwds)
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

def is_python_path(path, object_only=False):
    """Check if a string is a valid python path.

    Parameters
    ----------
    path : str
        String.
    object_only : bool
        Should `True` be returned only for object specifying paths.
    """
    m = _rx_pp.match(path)
    n_colons = path.count(':')
    if not m or n_colons > 1 or (object_only and n_colons != 1):
        return False
    return True

def iter_objects(path='.', obj_predicate=None, mod_predicate=None, skip_private=True,
                 skip_modules=('test', 'tests', 'doc', 'docs')):
    """Iter over all objects with optional predicate based filtering.

    Parameters
    ----------
    path : str
        Proper python module path.
    mod_predicate : callable or None
        Predicate function for filtering modules.
        Must take 3 arguments:
            - :py:class:`importlib.FileFinder` object.
            - module name
            - boolean telling it is a package
    obj_predictae : callable or None
        Predicate function for filtering objects.
    skip_private : bool
        Should private objects (starting with '_') be omitted.
    skip_modules : list of str
        List of module names to skip.
    """
    _path = path.replace('.', '', 1) if path.startswith('.') else path
    for finder, name, ispkg in walk_packages(path):
        if not name.startswith(_path):
            continue
        path_parts = name.split('.')
        for p in path_parts:
            if skip_private and p.startswith('_'):
                continue
            if skip_modules and p in skip_modules:
                continue
        if mod_predicate and not mod_predicate(finder, name, ispkg):
            continue
        module = import_python(name)
        for _, obj in module.__dict__.items():
            if obj_predicate and obj_predicate(obj):
                yield obj

def iter_classes(path='.', obj_predicate=None, **kwds):
    """Iter over all class objects with optional predicate based filtering.

    Uses the same parameters as
    :py:func:`{{ cookiecutter.repo_name }}.utils.iter_objects`.
    """
    def wrapped_obj_predicate(obj):
        """Wrapped object predicate function."""
        if not isinstance(obj, type):
            return False
        try:
            return obj_predicate(obj)
        except TypeError:
            return False
    yield from iter_objects(path, obj_predicate=wrapped_obj_predicate, **kwds)

def findone(iterable, predicate, ambiguous_match='ignore'):
    """Find first element satisfying a predicate.

    Parameters
    ----------
    iterable : Iterable
        Some iterable.
    predicate : callable
        Predicate function.
    ambiguous_match : {'ignore', 'raise', 'raise_if_not_unique'}
        Ignore any and return first matching object if 'ignore'.
        Raise if matching objects are not the same object if 'raise_if_not_unique'.
        Raise for any multiple match if 'raise'.

    Raises
    ------
    AmbiguousMatchError
        If `raise_if_ambiguous=True` and there is more than one match.
    """
    _vals = ['ignore', 'raise_if_not_unique', 'raise']
    if ambiguous_match not in _vals:
        raise ValueError(f"'ambiguous_match' must be on of: \'{', '.join(_vals)}\'")
    match = None
    for item in iterable:
        if predicate(item):
            if ambiguous_match != 'ignore':
                return item
            if match is None:
                match = item
            elif ambiguous_match == 'raise':
                raise AmbiguousMatchError.from_matches([item, match])
            elif match is not item:
                raise AmbiguousMatchError.from_matches([item, match])
    return match

def get_class(path_or_name, package=None, **kwds):
    """Get a class object by python path or name.

    Parameters
    ----------
    path_or_name : str
        Proper python path or class name.
    package : str or None
        Passed to
        :py:func:`{{ cookiecutter.repo_name }}.utils.import_python`.
    **kwds :
        Keyword arguments passed to
        :py:func:`{{ cookiecutter.repo_name }}.utils.iter_classes`.

    Raises
    ------
    ValueError
        If there are multiple matches, what may happen when using a class name
        instead of a fully qualified python path.
    """
    matches = []
    if is_python_path(path_or_name, object_only=True):
        return import_python(path_or_name, package=package)
    for clsobj in iter_classes(**kwds):
        if clsobj.__name__ == path_or_name and clsobj not in matches:
            matches.append(clsobj)
    if len(matches) == 1:
        return matches.pop()
    if len(matches) > 1:
        msg = f"Multiple matches ({', '.join(map(str, matches))})"
        raise ValueError(msg)
    return None
