"""Utility functions for CLI database module."""
from {{ cookiecutter.repo_name }}.utils.fetch import iter_db_connectors, iter_db_models
from {{ cookiecutter.repo_name }}.utils.fetch import get_db_model, get_importer
from {{ cookiecutter.repo_name }}.utils.fetch import get_persistence
from ..utils import pprint, show_unique
from {{ cookiecutter.repo_name }}.base.abc import AbstractMongoModel


def get_mongo_model(path_or_name, **kwds):
    """Get a *Mongoengine* model class.

    Parameters
    ----------
    path_or_name : str
        Proper python path or class name.
    **kwds :
        Keyword arguments passed to
        :py:function:`{{ cookiecutter.repo_name }}.utils.fetch.get_db_model`.
    """
    return get_db_model(path_or_name,
                        predicate=lambda x: isinstance(x, AbstractMongoModel), **kwds)

def show_db_connectors():
    """Show registered database connectors."""
    show_unique(iter_db_connectors())

def show_db_models():
    """Show registered database models."""
    show_unique(iter_db_models())

def show_mongo_models():
    """Show registered *MongoDB* models."""
    show_unique(iter_db_models(predicate=lambda x: isinstance(x, AbstractMongoModel)))

def show_mongo_model_schema(path_or_name):
    """Show *MongoDB* model schema.

    Parameters
    ----------
    path_or_name : str
        Proper python path or class name.
    """
    model = get_db_model(path_or_name, predicate=lambda x: isinstance(x, AbstractMongoModel))
    schema = model.get_schema().schema
    pprint(schema)
