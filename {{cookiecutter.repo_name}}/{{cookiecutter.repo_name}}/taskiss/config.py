"""Celery application config."""
import os as _os
from {{ cookiecutter.repo_name }}.config import cfg as _cfg
from {{ cookiecutter.repo_name }}.config import MODE as _mode

# Main URLs
broker_url = _cfg.getenvvar(_mode, 'celery_broker_url', fallback=None)
result_backend = _cfg.getenvvar(_mode, 'celery_result_backend', fallback=None)
# Included modules
include = ['{{cookiecutter.repo_name}}.taskiss.{{cookiecutter.taskmodule_name}}']
# Other settings
task_serializer = 'json'
result_serializer = 'json'
accept_content = ['json']
timezone = 'Europe/Warsaw'
enable_utc = True
# Task settings
task_track_started = True
task_ignore_result = True
task_soft_time_limit = 60*60
task_alaways_eager = \
    _cfg.getenvvar(_mode, 'celery_always_eager', convert_bool=True, fallback=False)
# Task routes
task_routes = {}
# Worker settings
worker_prefetch_multiplier = 1
worker_hijack_root_logger = True
