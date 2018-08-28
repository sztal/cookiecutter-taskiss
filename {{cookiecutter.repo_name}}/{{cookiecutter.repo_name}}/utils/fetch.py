"""Utilities for fetching various kinds of classes and objects."""
from {{ cookiecutter.repo_name }}.utils import iter_objects, iter_classes
from {{ cookiecutter.repo_name }}.utils import is_python_path, import_python
from {{ cookiecutter.repo_name }}.base.abc import AbstractDBConnector, AbstractDBModel
from {{ cookiecutter.repo_name }}.base.abc import AbstractDBImporter, AbstractPersistence
from {{ cookiecutter.repo_name }}.persistence import BasePersistence
from {{ cookiecutter.repo_name }}.persistence.db import BaseDBModelMixin
from {{ cookiecutter.repo_name }}.persistence.importers import BaseDBImporter


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
    """Get a database model class by python path or name.

    Parameters
    ----------
    path_or_name : str
        Proper python path or class name.
    package : str or None
        Passed to
        :py:function:`{{ cookiecutter.repo_name }}.utils.import_python`.
    **kwds :
        Keyword arguments passed to
        :py:function:`{{ cookiecutter.repo_name }}.utils.fetch.iter_db_models`.
    """
    if is_python_path(path_or_name, object_only=True):
        return import_python(path_or_name, package=package)
    for model in iter_db_models(**kwds):
        if model.__name__ == path_or_name:
            return model

def iter_db_importers(predicate=None):
    """Iter over available db importers."""
    obj_predicate = lambda o: \
        issubclass(o, AbstractDBImporter) and issubclass(o, BaseDBImporter) \
        and (predicate(o) if predicate else True)
    yield from iter_classes('.{{ cookiecutter.repo_name }}', obj_predicate=obj_predicate)

def get_db_importer(path_or_name, package=None, **kwds):
    """Get a database importer class by python path or name.

    Parameters
    ----------
    path_or_name : str
        Proper python path or class name.
    package : str or None
        Passed to
        :py:function:`{{ cookiecutter.repo_name }}.utils.import_python`.
    **kwds :
        Keyword arguments passed to
        :py:function:`{{ cookiecutter.repo_name }}.utils.fetch.iter_db_importers`.
    """
    if is_python_path(path_or_name, object_only=True):
        return import_python(path_or_name, package=package)
    for importer in iter_db_importers(**kwds):
        if importer.__name__ == path_or_name:
            return importer

def iter_persistence(predicate=None):
    """Iter over available persistence classes."""
    obj_predicate = lambda o: \
        issubclass(o, AbstractPersistence) and issubclass(o, BasePersistence) \
        and (predicate(o) if predicate else True)
    yield from iter_classes('.{{ cookiecutter.repo_name }}', obj_predicate=obj_predicate)

def get_persistence(path_or_name, package=None, **kwds):
    """Get a persistence class by python path or name.

    Parameters
    ----------
    path_or_name : str
        Proper python path or class name.
    package : str or None
        Passed to
        :py:function:`{{ cookiecutter.repo_name }}.utils.import_python`.
    **kwds :
        Keyword arguments passed to
        :py:function:`{{ cookiecutter.repo_name }}.utils.fetch.iter_persistence`.
    """
    if is_python_path(path_or_name, object_only=True):
        return import_python(path_or_name, package=package)
    for persistence in iter_persistence(**kwds):
        if persistence.__name__ == path_or_name:
            return persistence
