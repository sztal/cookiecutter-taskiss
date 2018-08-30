"""Test cases for various utility functions."""
import pytest
import {{ cookiecutter.repo_name }}
import {{ cookiecutter.repo_name }}.taskiss
import {{ cookiecutter.repo_name }}.config as cfg
import {{ cookiecutter.repo_name }}.utils.path as path
from {{ cookiecutter.repo_name }}.persistence.importers import BaseImporter
from {{ cookiecutter.repo_name }}.utils import import_python, iter_objects
from {{ cookiecutter.repo_name }}.base.abc import AbstractInterfaceMetaclass, AbstractImporterMetaclass


@pytest.mark.parametrize('path,package,exp', [
    ('{{ cookiecutter.repo_name }}', None, {{ cookiecutter.repo_name }}),
    ('{{ cookiecutter.repo_name }}.config:cfg', None, cfg.cfg),
    ('.path', '{{ cookiecutter.repo_name }}.utils', path),
    ('.path:is_file', '{{ cookiecutter.repo_name }}.utils', path.is_file)

])
def test_import_python(path, package, exp):
    """Test cases for `import_python`."""
    res = import_python(path, package)
    assert res == exp


obj_predicate1 = lambda x: isinstance(x, AbstractImporterMetaclass)
obj_predicate2 = lambda x: isinstance(x, AbstractInterfaceMetaclass)

@pytest.mark.parametrize('path,obj_predicate', [
    ('{{ cookiecutter.repo_name }}.persistence', obj_predicate1),
    ('{{ cookiecutter.repo_name }}', obj_predicate2)
])
def test_iter_objects(path, obj_predicate, mod_predicate):
    """Test cases for `iter_objects`."""
    objects = iter_objects(path, obj_predicate, mod_predicate=mod_predicate)
    for obj in objects:
        assert obj_predicate(obj)
