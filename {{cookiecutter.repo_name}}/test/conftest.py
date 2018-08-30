"""Shared configuration and fixtures of the test suite.

In principle tasks are tested in two different ways.
Their main logic (defined in `.run()`) method can be in most cases
tested in idempotent and isolated unit tests, although sometimes
it may be necessary to use mocking and/or patching.

Tests can also be run within working
"""
import os
import pytest
from click.testing import CliRunner
from {{ cookiecutter.repo_name }} import taskiss
from {{ cookiecutter.repo_name }}.config import cfg, MODE
from {{ cookiecutter.repo_name }}.taskiss.scheduler import Scheduler
from {{ cookiecutter.repo_name }}.config.taskiss import include
# Import tasks only if taskiss object is defined
if taskiss:
        import {{ cookiecutter.repo_name }}.tasks as _tasks

# Custom options --------------------------------------------------------------

def pytest_addoption(parser):
    """Additional custom `pytest` command line options."""
    parser.addoption(
        '--all', action='store_true', default=False,
        help="Run all tests. Database test still need to be enabled in the configuration."
    )
    parser.addoption(
        '--run-tasks', action='store_true', default=False,
        help="Run task tests."
    )
    parser.addoption(
        '--run-mongo', action='store_true', default=True,
        help="Run tests dependent on MongoDB."
    )

def pytest_collection_modifyitems(config, items):
    """Modify test runner behavior based on `pytest` settings."""
    use_mongo = cfg.getenvvar(MODE, 'use_mongo', fallback=True, convert_bool=True)
    use_celery = cfg.getenvvar(MODE, 'use_celery', fallback=True, convert_bool=True)
    run_all = config.getoption('--all')
    run_tasks = use_celery and (config.getoption('--run-tasks') or run_all)
    run_mongo = use_mongo and (config.getoption('--run-mongo') or run_all)
    if not run_tasks:
        skip_tasks = pytest.mark.skip(
            reason="need --run-tasks to run and 'USE_CELERY' enabled to run."
        )
        for item in items:
            if "task" in item.keywords:
                item.add_marker(skip_tasks)
    if not run_mongo:
        skip_db_tasks = pytest.mark.skip(
            reason="need --run-mongo and envvar 'USE_MONGO' enabled to run."
        )
        for item in items:
            if "mongo" in item.keywords:
                item.add_marker(skip_db_tasks)

# Fixtures --------------------------------------------------------------------

@pytest.fixture(scope='session')
def taskiss():
    """Fixture: *Taskiss* application object."""
    if taskiss:
        taskiss.scheduler.get_registered_tasks()
        taskiss.scheduler.build_dependency_graph()
    return taskiss

@pytest.fixture(scope='session')
def tasks():
    """Fixture: *Taskiss* tasks."""
    return _tasks

@pytest.fixture(scope='session')
def celery_config():
    """Fixture: basic *Celery* config."""
    return {
        'broker_url':
            os.environ.get('CELERY_TEST_BROKER_URL', 'pyamqp://'),
        'result_backend':
            os.environ.get('CELERY_TEST_RESULT_BACKEND', 'redis://127.0.0.1'),
        'include': ['{{cookiecutter.repo_name}}.tasks'],
        'task_serializer': 'json',
        'result_serializer': 'json',
        'accept_content': ['json'],
        'enable_utc': True
    }

@pytest.fixture(scope='session')
def scheduler():
    """Fixture: *Taskiss* scheduler object."""
    scheduler = Scheduler(include)
    scheduler.get_registered_tasks()
    scheduler.build_dependency_graph()
    return scheduler

@pytest.fixture(scope='session')
def mod_predicate():
    """Fixture: module predicate for handling test when some app parts are disabled."""
    def _mod_predicate(finder, name, ispkg):
        """Module predicate function."""
        celery = cfg.getenvvar(MODE, 'use_celery', fallback=True, convert_bool=True)
        mongo = cfg.getenvvar(MODE, 'use_mongo', fallback=True, convert_bool=True)
        if not celery:
            for dep in include:
                if name.startswith(dep):
                    return False
        mongo_path = '{{ cookiecutter.repo_name }}.persistence.db.mongo'
        if not mongo and name.startswith(mongo_path):
            return False
        return True
    return _mod_predicate

@pytest.fixture
def cli_runner():
    """Command-line test runner."""
    return CliRunner()
