"""Application specific utilities."""
from {{ cookiecutter.repo_name }}.utils import iter_objects
from {{ cookiecutter.repo_name }}.base.abc import AbstractDBConnector, AbstractDBModel
from {{ cookiecutter.repo_name }}.persistence.db import BaseDBModelMixin
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
    def obj_predicate(x):
        """Class object predicate."""
        if not isinstance(x, type):
            return False
        try:
            return issubclass(x, AbstractDBModel) \
            and issubclass(x, BaseDBModelMixin)
        except TypeError:
            return False

    models = \
        iter_objects('.{{ cookiecutter.repo_name }}', obj_predicate=obj_predicate)
    for model in models:
        if predicate and not predicate(model):
            continue
        yield model
