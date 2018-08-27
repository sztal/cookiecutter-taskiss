"""Test cases for various utility functions."""
import pytest
import {{ cookiecutter.repo_name }}
import {{ cookiecutter.repo_name }}.taskiss
import {{ cookiecutter.repo_name }}.config as cfg
import {{ cookiecutter.repo_name }}.utils.path as path
from {{ cookiecutter.repo_name }}.utils import import_python


@pytest.mark.parametrize('path,package,exp', [
    ('{{ cookiecutter.repo_name }}', None, {{ cookiecutter.repo_name }}),
    ('{{ cookiecutter.repo_name }}.config:cfg', None, cfg.cfg),
    ('{{ cookiecutter.repo_name }}.taskiss', None, {{ cookiecutter.repo_name }}.taskiss),
    ('{{ cookiecutter.repo_name }}.taskiss:taskiss', None, {{ cookiecutter.repo_name }}.taskiss.taskiss),
    ('.path', '{{ cookiecutter.repo_name }}.utils', path),
    ('.path:is_file', '{{ cookiecutter.repo_name }}.utils', path.is_file)

])
def test_get_python(path, package, exp):
    """Test cases for `get_python`."""
    res = import_python(path, package)
    assert res == exp
