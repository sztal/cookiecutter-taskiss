"""Utility functions for CLI database module."""
from {{ cookiecutter.repo_name }}.utils.app import iter_db_connectors, iter_db_models
from {{ cookiecutter.repo_name }}.utils.app import iter_db_importers
from {{ cookiecutter.repo_name }}.utils.app import get_db_model
from {{ cookiecutter.repo_name }}.cli.utils import pprint
from {{ cookiecutter.repo_name }}.base.abc import AbstractMongoModel

def show_unique(iterator):
    """Show unique values in an iterator."""
    shown = []
    for item in iterator:
        if item in shown:
            continue
        shown.append(item)
        pprint(item)

def show_db_connectors():
    """Show registered database connectors."""
    show_unique(iter_db_connectors())

def show_db_models():
    """Show registered database models."""
    show_unique(iter_db_models())

def show_mongo_models():
    """Show registered *MongoDB* models."""
    show_unique(iter_db_models(predicate=lambda x: issubclass(x, AbstractMongoModel)))

def show_mongo_model_schema(path_or_name):
    """Show *MongoDB* model schema.

    Parameters
    ----------
    path_or_name : str
        Proper python path or class name.
    """
    model = get_db_model(path_or_name,
                         predicate=lambda x: issubclass(x, AbstractMongoModel))
    schema = model.get_schema().schema
    pprint(schema)

def show_db_importers():
    """Show registered database importers."""
    show_unique(iter_db_importers())
