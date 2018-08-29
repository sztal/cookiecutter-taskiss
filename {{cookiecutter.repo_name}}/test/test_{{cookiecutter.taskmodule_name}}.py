"""Tests for `{{ cookiecutter.taskmodule_name }}` module.

This is module for idempotent task tests.
In other words, here `.run()` methods should be tested.

Tests need running Celery worker to run. Fixtures like `celery_worker`
are avoided, since they do not always work well.
"""
import os
import pytest

# Unit tests class ------------------------------------------------------------

@pytest.mark.task
class TestTasksEndToEnd:
    """End-to-end not-idempotent task tests."""
    timeout = 30

    def test_t5(self, {{ cookiecutter.taskmodule_name }}):
        """Test case."""
        t5 = {{ cookiecutter.taskmodule_name}}.t5
        res = t5.delay(x=10, y=10).get(timeout=self.timeout)
        assert res == { 'n': 100 }
