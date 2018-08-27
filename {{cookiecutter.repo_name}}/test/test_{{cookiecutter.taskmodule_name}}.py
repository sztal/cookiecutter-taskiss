"""Tests for `{{ cookiecutter.taskmodule_name }}` module.

This is module for idempotent task tests.
In other words, here `.run()` methods should be tested.

Tests need running Celery worker to run. Fixtures like `celery_worker`
are avoided, since they do not always work well.
"""
import os
import pytest
from {{ cookiecutter.repo_name }}.taskiss.{{ cookiecutter.taskmodule_name }} import taskiss, t5

if os.environ.get('RUNTIME_MODE', 'DEV').lower() != 'dev':
    raise ValueError("Non-idempotent tests may be run only with envvar 'RUNTIME_MODE = dev'")

# Unit tests class ------------------------------------------------------------

@pytest.mark.task
class TestTasksEndToEnd:
    """End-to-end not-idempotent task tests."""
    timeout = 30
    taskiss.scheduler.get_registered_tasks()
    taskiss.scheduler.build_dependency_graph()

    def test_t5(self):
        """Test case."""
        res = t5.delay(x=10, y=10).get(timeout=self.timeout)
        assert res == { 'n': 100 }
