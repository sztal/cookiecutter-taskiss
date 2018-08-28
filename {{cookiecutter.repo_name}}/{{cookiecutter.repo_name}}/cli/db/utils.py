"""Utility functions for CLI database module."""
from {{ cookiecutter.repo_name }}.utils.fetch import iter_db_connectors, iter_db_models
from {{ cookiecutter.repo_name }}.utils.fetch import iter_db_importers
from {{ cookiecutter.repo_name }}.utils.fetch import get_db_model, get_db_importer
from {{ cookiecutter.repo_name }}.cli.utils import pprint, show_unique
from {{ cookiecutter.repo_name }}.base.abc import AbstractMongoModel


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

def show_db_importer_schema(path_or_name):
    """Show database importer schema.

    Parameters
    ----------
    path_or_name : str
        Proper python path or class name.
    """
    importer = get_db_importer(path_or_name)
    schema = importer.get_schema().schema
    pprint(schema)

def run_db_importer(importer, persistence, **kwds):
    """Run database data importer.

    Parameters
    ----------
    importer : str
        Importer class specified as a fully qualified python path
        or a class name.
    persistence : str
        Persistence class specified as a fully qualified python path
        or a class name.
    **kwds :
        Keyword arguments passed both to the importer and the persistence.
        This can be done without any risk thanks to the interfaces.
    """
    pass

