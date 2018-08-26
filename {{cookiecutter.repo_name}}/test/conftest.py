"""Shared configuration and fixtures of the test suite.

In principle tasks are tested in two different ways.
Their main logic (defined in `.run()`) method can be in most cases
tested in idempotent and isolated unit tests, although sometimes
it may be necessary to use mocking and/or patching.

Tests can also be run within working
"""
import os
import pytest
from {{ cookiecutter.repo_name }} import MODE
from {{ cookiecutter.repo_name }}.cfg import cfg
from {{ cookiecutter.repo_name }}.taskiss.scheduler import Scheduler
from {{ cookiecutter.repo_name }}.taskiss.config import include

# Custom options --------------------------------------------------------------

def pytest_addoption(parser):
    """Additional custom `pytest` command line options."""
    parser.addoption(
        '--run-tasks', action='store_true', default=False,
        help="Run task tests."
    )
    parser.addoption(
        '--run-db', action='store_true', default=True,
        help="Run database-dependent tests."
    )

def pytest_collection_modifyitems(config, items):
    """Modify test runner behavior based on `pytest` settings."""
    if not config.getoption('--run-tasks'):
        skip_tasks = pytest.mark.skip(
            reason="need --run-tasks to run"
        )
        for item in items:
            if "task" in item.keywords:
                item.add_marker(skip_tasks)
    if not config.getoption('--run-db') or not cfg.getenvvar(MODE, 'db_use', fallback=True):
        skip_db_tasks = pytest.mark.skip(
            reason="nee --run-db and envvar 'DB_USE' enabled to run"
        )
        for item in items:
            if "db" in item.keywords:
                item.add_marker(skip_db_tasks)

# Fixtures --------------------------------------------------------------------

@pytest.fixture(scope='session')
def celery_config():
    """Fixture: basic _Celery_ config."""
    return {
        'broker_url':
            os.environ.get('CELERY_TEST_BROKER_URL', 'pyamqp://'),
        'result_backend':
            os.environ.get('CELERY_TEST_RESULT_BACKEND', 'redis://127.0.0.1'),
        'include': ['{{cookiecutter.repo_name}}.{{cookiecutter.taskdir_name}}'],
        'task_serializer': 'json',
        'result_serializer': 'json',
        'accept_content': ['json'],
        'enable_utc': True
    }

@pytest.fixture(scope='session')
def scheduler():
    """Fixture: _Taskiss_ scheduler object."""
    scheduler = Scheduler(include)
    scheduler.get_registered_tasks()
    scheduler.build_dependency_graph()
    return scheduler
