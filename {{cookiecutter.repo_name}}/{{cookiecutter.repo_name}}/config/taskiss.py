"""*Taskiss-Celery* application config."""
from . import cfg as _cfg
from . import MODE as _mode

# Main URLs
broker_url = _cfg.getenvvar(_mode, 'celery_broker_url', fallback=None)
result_backend = _cfg.getenvvar(_mode, 'celery_result_backend', fallback=None)
# Included modules
include = ['{{cookiecutter.repo_name}}.tasks']
# Other settings
task_serializer = 'json'
result_serializer = 'json'
accept_content = ['json']
timezone = 'Europe/Warsaw'
enable_utc = True
# Task settings
task_track_started = True
task_ignore_result = False
task_soft_time_limit = 60*60
task_alaways_eager = _cfg.getboolean(_mode, 'celery_always_eager', fallback=False)
# Task routes
task_routes = {}
# Worker settings
worker_prefetch_multiplier = 1
worker_hijack_root_logger = True
