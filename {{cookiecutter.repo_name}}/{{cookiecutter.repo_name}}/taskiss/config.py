"""Celery application config."""
import os as _os
from {{ cookiecutter.repo_name }} import cfg as _cfg
from {{ cookiecutter.repo_name }} import MODE as _mode

# Main URLs
broker_url = _os.environ[_cfg.get(_mode, 'celery_broker_url')]
result_backend = _os.environ[_cfg.get(_mode, 'celery_result_backend')]
# Included modules
include = ['{{cookiecutter.repo_name}}.taskiss.{{cookiecutter.taskdir_name}}']
if _mode.lower() == 'dev':
    include.append('test.tasks')
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
# Task routes
task_routes = {}
# Worker settings
worker_prefetch_multiplier = 1
worker_hijack_root_logger = True
