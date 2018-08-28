"""Test cases for various utility functions."""
import pytest
import {{ cookiecutter.repo_name }}
import {{ cookiecutter.repo_name }}.taskiss
import {{ cookiecutter.repo_name }}.config as cfg
import {{ cookiecutter.repo_name }}.utils.path as path
from {{ cookiecutter.repo_name }}.persistence.importers import BaseImporter
from {{ cookiecutter.repo_name }}.utils import import_python, iter_objects
from {{ cookiecutter.repo_name }}.base.abc import AbstractInterface


@pytest.mark.parametrize('path,package,exp', [
    ('{{ cookiecutter.repo_name }}', None, {{ cookiecutter.repo_name }}),
    ('{{ cookiecutter.repo_name }}.config:cfg', None, cfg.cfg),
    ('{{ cookiecutter.repo_name }}.taskiss', None, {{ cookiecutter.repo_name }}.taskiss),
    ('{{ cookiecutter.repo_name }}.taskiss:taskiss', None, {{ cookiecutter.repo_name }}.taskiss.taskiss),
    ('.path', '{{ cookiecutter.repo_name }}.utils', path),
    ('.path:is_file', '{{ cookiecutter.repo_name }}.utils', path.is_file)

])
def test_import_python(path, package, exp):
    """Test cases for `import_python`."""
    res = import_python(path, package)
    assert res == exp


obj_predicate1 = lambda x: isinstance(x, type) and issubclass(x, BaseImporter)
obj_predicate2 = lambda x: isinstance(x, type) and issubclass(x, AbstractInterface)

@pytest.mark.parametrize('path,mod_predicate,obj_predicate', [
    ('{{ cookiecutter.repo_name }}.persistence', None, obj_predicate1),
    ('{{ cookiecutter.repo_name }}', None, AbstractInterface)
])
def test_iter_objects(path, mod_predicate, obj_predicate):
    """Test cases for `iter_objects`."""
    objects = iter_objects(path, mod_predicate, obj_predicate)
    for obj in objects:
        assert obj_predicate(obj)
