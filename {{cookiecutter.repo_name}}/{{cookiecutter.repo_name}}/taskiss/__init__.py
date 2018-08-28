"""Main _Taskiss_ module.

Here the Celery-Taskiss application object is defined.
"""
from {{ cookiecutter.repo_name }}.config import MODE, cfg
from {{ cookiecutter.repo_name }}.taskiss.basecls import Taskiss  # noqa: F401
from {{ cookiecutter.repo_name }}.taskiss.taskcls import TaskissTask

taskiss = None
if cfg.getenvvar(MODE, 'use_celery', fallback=True, convert_bool=True):
    taskiss = Taskiss('{{cookiecutter.repo_name}}',
                config_source='{{cookiecutter.repo_name}}.taskiss.config',
                task_cls=TaskissTask)
    taskiss.setup_scheduler()
