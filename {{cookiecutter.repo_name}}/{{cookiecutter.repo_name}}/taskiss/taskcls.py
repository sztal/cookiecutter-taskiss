"""Custom Celery task classes and decorators."""
from collections import defaultdict, Mapping
from logging import getLogger
from celery import Task
from celery.worker.request import Request
from {{ cookiecutter.repo_name }}.taskiss.utils import merge_results


class TaskissRequest(Request):
    """_Taskiss_ request class."""
    pass


class TaskissTask(Task):
    """_Taskiss_ task class.

    This is an extension of the base :py:class:`celery.Task` class
    that restructures incoming arguments to comply to the task
    main function signature.
    """
    Request = TaskissRequest
    logger = getLogger('taskiss')

    def __call__(self, *args, args_to_kwds=False,
                 raise_when_ambiguous_args=True, **kwds):
        """Task call method.

        Parameters
        ----------
        *args :
            Positional arguments passed to the main task function.
        args_to_kwds : bool
            Should positional arguments be merged with kwds.
            Otherwise they are dropped.
        raise_when_ambiguous_args : bool
            Should error be raised with ambiguous arguments are passed.
            If `False` then ambiguous args are overwritten.
        **kwds :
            Keyword arguments passed to the main task function.
        """
        if args_to_kwds and args:
            args = merge_results(args, raise_when_ambiguous_args=raise_when_ambiguous_args)
            kwds = { **kwds, **args }
        res = super().__call__(**kwds)
        if isinstance(res, Mapping):
            return self.make_results(**res)
        return self.make_results(res)

    def make_results(self, *args, **kwds):
        """Organize results in the standard _Taskiss_ format.

        Notes
        -----
        Since order of task execution is not guaranteed in _Celery_
        the _Taskiss_ communication protocol uses key-value pairs
        only represented as dictionaries with default value of `None`.

        If positional arguments are passed, then they are assigned
        to the same name as the task name.
        However, usage of positional arguments is highly discouraged.

        Parameters
        ----------
        *args :
            Positional arguments.
        **kwds :
            Keyword arguments.
        """
        res = defaultdict(lambda: None, **kwds)
        if args:
            res[self.name] = args
        return res
