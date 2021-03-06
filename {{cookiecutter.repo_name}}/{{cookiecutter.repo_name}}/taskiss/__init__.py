"""Main *Taskiss* module.

`Taskiss` is a subclass of standard :py:class:`celery.Celery` class that
adds a :py:class:`{{ cookiecutter.repo_name }}.scheduler.Scheduler`
component to it.
"""
from celery import Celery
from .taskcls import TaskissTask
from .scheduler import Scheduler


class Taskiss(Celery):
    """_Taskiss_ application object.

    In all respects this class behaves exactly like standard
    :py:class:`celery.Celery` objects. The only difference is that
    it defines an additional `scheduler` attribute, which is an
    instance of :py:cass:`{{ cookiecutter.repo_name }}.scheduler.Scheduler`.
    The scheduler is used to chain dependent tasks and prevent circular
    task dependencies from being defined.

    Attributes
    ----------
    scheduler : `{{ cookiecutter.repo_name }}.Scheduler`
        Scheduler object.
    """
    def __init__(self, *args, task_cls=TaskissTask, **kwds):
        """Initialization method.

        Parameters
        ----------
        *args :
            Positional arguments passed to `Celery` init method.
        task_cls : :py:class:`celery.Task`
            Default *Celery* task class.
            Defaults to :py:class:`.taskcls.TaskissTask`.
        **kwds :
            Keyword arguments passed to `Celery` init method.

        See Also
        --------
        celery.Celery : _Celery_ application class
        {{ cookiecutter.repo_name }}.scheduler.Scheduler : _Taskiss_ scheduler class
        """
        super().__init__(*args, task_cls=task_cls, **kwds)
        self.scheduler = None

    def setup_scheduler(self, **kwds):
        """Setup scheduler object.

        Scheduler setup must be done outside of the `__init__` method
        in order to properly discover all tasks.

        Parameters
        ----------
        **kwds :
            Keyword arguments passed to the _Scheduler_ init method.
        """
        self.scheduler = Scheduler(self.conf['include'], **kwds)
