"""Taskiss-Celery utility functions."""
from collections import defaultdict, Mapping
from {{ cookiecutter.repo_name }}.taskiss.exceptions import AmbiguousTaskArgumentsError

def make_signature(task, *args):
    """Make task execution signature.

    Parameters
    ----------
    task : celery.Task
        Object inheriting from :py:class:`celery.Task`.
    """
    if getattr(task, 'immutable', False):
        return task.si(*args)
    return task.s(*args)

def merge_results(*args, raise_ambiguous_args=True):
    """Merge result dicts.

    Parameters
    ----------
    *args :
        Sequence of dict-like datasets.
    raise_ambiguous_args : bool
        Should error be raised with ambiguous arguments are passed.
        If `False` then ambiguous args are overwritten.
    """
    results = {}
    ambiguous = defaultdict(list)
    _args = []
    for obj in args:
        if not isinstance(obj, Mapping):
            _args.append(obj)
            continue
        if '_args' in obj:
            _args = [ *_args, *obj['_args'] ]
        if raise_ambiguous_args:
            for key in obj:
                if key in results and results[key] != obj[key]:
                    ambiguous[key].append(results[key], obj[key])
        try:
            results = { **results, **obj }
        except (TypeError, AttributeError, ValueError):
            raise TypeError("Can not merge {} with {}".format(results, obj))
    if ambiguous:
        raise AmbiguousTaskArgumentsError(ambiguous)
    if _args:
        results.update(_args=_args)
    return results
