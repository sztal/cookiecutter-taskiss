"""Utilities for fetching various kinds of classes and objects."""
from {{ cookiecutter.repo_name }}.utils import iter_objects, iter_classes, findone
from {{ cookiecutter.repo_name }}.utils import is_python_path, import_python
from {{ cookiecutter.repo_name }}.base.abc import AbstractDBConnector, AbstractDBModel, AbstractDBMixin
from {{ cookiecutter.repo_name }}.base.abc import AbstractImporterMetaclass, AbstractPersistenceMetaclass



def iter_db_connectors(predicate=None):
    """Iter over available db connectors."""
    obj_predicate=lambda x: isinstance(x, AbstractDBConnector) \
        and (predicate(o) if predicate else True)
    yield from iter_objects('.{{ cookiecutter.repo_name }}',
                               obj_predicate=obj_predicate)

def iter_db_models(predicate=None):
    """Iter over available db models."""
    obj_predicate = lambda o: isinstance(o, AbstractDBModel) \
        and issubclass(o, AbstractDBMixin) \
        and (predicate(o) if predicate else True)
    yield from iter_classes('.{{ cookiecutter.repo_name }}',
                            obj_predicate=obj_predicate)

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
    models = iter_db_models(**kwds)
    return findone(models, lambda x: x.__name__ == path_or_name,
                   ambiguous_match='raise_if_not_unique')

def iter_importers(predicate=None):
    """Iter over available db importers."""
    obj_predicate = lambda o: isinstance(o, AbstractImporterMetaclass) \
        and (predicate(o) if predicate else True)
    yield from iter_classes('.{{ cookiecutter.repo_name }}',
                            obj_predicate=obj_predicate)

def get_importer(path_or_name, package=None, **kwds):
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
        :py:function:`{{ cookiecutter.repo_name }}.utils.fetch.iter_importers`.
    """
    if is_python_path(path_or_name, object_only=True):
        return import_python(path_or_name, package=package)
    importers = iter_importers(**kwds)
    return findone(importers, lambda x: x.__name__ == path_or_name,
                   ambiguous_match='raise_if_not_unique')

def iter_persistence(predicate=None):
    """Iter over available persistence classes."""
    obj_predicate = lambda o: isinstance(o, AbstractPersistenceMetaclass) \
        and (predicate(o) if predicate else True)
    yield from iter_classes('.{{ cookiecutter.repo_name }}',
                            obj_predicate=obj_predicate)

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
    persistence = iter_persistence(**kwds)
    return findone(persistence, lambda x: x.__name__ == path_or_name,
                   ambiguous_match='raise_if_not_unique')
