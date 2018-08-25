"""Taskiss-Celery utility functions."""
from collections import defaultdict
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

def merge_results(*args, raise_when_ambiguous_args=True):
    """Merge result dicts.

    Parameters
    ----------
    *args :
        Sequence of dict-like datasets.
    raise_when_ambiguous_args : bool
        Should error be raised with ambiguous arguments are passed.
        If `False` then ambiguous args are overwritten.
    """
    results = {}
    ambiguous = defaultdict(list)
    for dct in args:
        for key in dct:
            if key in results and results[key] != dct[key]:
                ambiguous[key].append(results[key], dct[key])
        try:
            results = { **results, **dct }
        except (TypeError, AttributeError, ValueError):
            raise TypeError("Can not merge {} with {}".format(results, dct))
    if ambiguous:
        raise AmbiguousTaskArgumentsError(ambiguous)
    return results
