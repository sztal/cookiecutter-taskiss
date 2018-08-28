"""Test cases for :py:module:`{{ cookiecutter.repo_name }}.utils.fetch`."""
import pytest
from {{ cookiecutter.repo_name }}.cli.utils import to_console
from {{ cookiecutter.repo_name }}.utils.fetch import iter_db_connectors, iter_db_models
from {{ cookiecutter.repo_name }}.utils.fetch import iter_importers, iter_persistence
from {{ cookiecutter.repo_name }}.utils.fetch import get_db_model
from {{ cookiecutter.repo_name }}.utils.fetch import get_importer
from {{ cookiecutter.repo_name }}.utils.fetch import get_persistence
from {{ cookiecutter.repo_name }}.persistence.db.mongo.models import ExampleMongoModel
from {{ cookiecutter.repo_name }}.persistence.importers import JSONLinesImporter
from {{ cookiecutter.repo_name }}.persistence import DBPersistence


def exec_and_catch(func):
    """Test runner helper."""
    try:
        func()
    except Exception as exc:
        pytest.fail(str(exc))

@pytest.mark.parametrize('unique', [(True,), (False,)])
def test_iter_db_connectors(unique):
    """Test case for `iter_db_connectors`."""
    exec_and_catch(lambda: to_console(iter_db_connectors(), unique=unique))
    exec_and_catch(lambda: to_console(iter_db_models(), unique=unique))
    exec_and_catch(lambda: to_console(iter_importers(), unique=unique))
    exec_and_catch(lambda: to_console(iter_persistence(), unique=unique))

@pytest.mark.parametrize('path_or_name,exp', [
    ('ExampleMongoModel', ExampleMongoModel),
    ('{{ cookiecutter.repo_name }}.persistence.db.mongo.models:ExampleMongoModel', ExampleMongoModel)
])
def test_get_db_model(path_or_name, exp):
    """Test case for `get_db_model`."""
    res = get_db_model(path_or_name)
    assert res is exp

@pytest.mark.parametrize('path_or_name,exp', [
    ('JSONLinesImporter', JSONLinesImporter),
    ('{{ cookiecutter.repo_name }}.persistence.importers:JSONLinesImporter', JSONLinesImporter)
])
def test_get_importer(path_or_name, exp):
    """Test case for `get_importer`."""
    res = get_importer(path_or_name)
    assert res is exp

@pytest.mark.parametrize('path_or_name,exp', [
    ('DBPersistence', DBPersistence),
    ('{{ cookiecutter.repo_name }}.persistence:DBPersistence', DBPersistence)
])
def test_get_persistence(path_or_name, exp):
    """Test case for `get_persistence`."""
    res = get_persistence(path_or_name)
    assert res is exp
