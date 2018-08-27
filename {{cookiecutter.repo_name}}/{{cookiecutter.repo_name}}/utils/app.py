"""Application specific utilities."""
from {{ cookiecutter.repo_name }}.utils import iter_objects, iter_classes
from {{ cookiecutter.repo_name }}.utils import is_python_path, import_python
from {{ cookiecutter.repo_name }}.base.abc import AbstractDBConnector, AbstractDBModel
from {{ cookiecutter.repo_name }}.base.abc import AbstractDBImporter
from {{ cookiecutter.repo_name }}.persistence.db import BaseDBModelMixin
from {{ cookiecutter.repo_name }}.persistence.importers import BaseDBImporter
from {{ cookiecutter.repo_name }}.config import cfg, MODE, ROOT_PATH


# Base path getter ------------------------------------------------------------

def get_data_path(section, *args, **kwds):
    """Get path for the project data directory.

    Parameters
    ----------
    section : str
        Name of data section as defined in the config.
    *args :
        Path components.
    **kwds :
        Other arguments passed to `os.makedirs`.
    """
    dirpath = cfg.get(MODE, section)
    path = os.path.join(ROOT_PATH, dirpath, *args)
    return make_path(path, **kwds)

def get_rawdata_path(*args, **kwds):
    """Get rawdata project directory path.

    Parameters
    ----------
    *args :
        Path components.
    **kwds :
        Arguments passed to `get_data_path`.
    """
    return get_data_path('path_data_rawdata', *args, **kwds)

def get_persistence_path(*args, **kwds):
    """Get data persistence project directory path.

    Parameters
    ----------
    *args :
        Path components.
    **kwds :
        Arguments passed to `get_data_path`.
    """
    return get_data_path('path_data_persistence', *args, **kwds)

# -----------------------------------------------------------------------------

def iter_db_connectors(predicate=None):
    """Iter over available db connectors."""
    connections = iter_objects(
        path='.{{ cookiecutter.repo_name }}',
        obj_predicate=lambda x: isinstance(x, AbstractDBConnector),
    )
    for conn in connections:
        if predicate and not predicate(conn):
            continue
        yield conn

def iter_db_models(predicate=None):
    """Iter over available db models."""
    obj_predicate = lambda o: \
        issubclass(o, AbstractDBModel) and issubclass(o, BaseDBModelMixin) \
        and (predicate(o) if predicate else True)
    yield from iter_classes('.{{ cookiecutter.repo_name }}', obj_predicate=obj_predicate)

def get_db_model(path_or_name, package=None, **kwds):
    """Get a database model object by python path or name.

    Parameters
    ----------
    path_or_name : str
        Proper python path or class name.
    package : str or None
        Passed to
        :py:function:`{{ cookiecutter.repo_name }}.utils.import_python`.
    **kwds :
        Keyword arguments passed to
        :py:function:`{{ cookiecutter.repo_name }}.utils.app.iter_db_models`.
    """
    if (path_or_name.count('.') >= 1 or path_or_name.count(':') == 1) \
    and is_python_path(path_or_name):
        return import_python(path_or_name)
    for model in iter_db_models(**kwds):
        if model.__name__ == path_or_name:
            return model

def iter_db_importers(predicate=None):
    """Iter over available db importers."""
    obj_predicate = lambda o: \
        issubclass(o, AbstractDBImporter) and issubclass(o, BaseDBImporter) \
        and (predicate(o) if predicate else True)
    yield from iter_classes('.{{ cookiecutter.repo_name }}', obj_predicate=obj_predicate)

