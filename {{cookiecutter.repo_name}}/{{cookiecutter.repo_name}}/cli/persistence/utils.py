"""Utilities for persistence classes command-line interface."""
from {{ cookiecutter.repo_name }}.utils.fetch import iter_persistence, get_persistence
from {{ cookiecutter.repo_name }}.cli.utils import pprint, show_unique


def show_persistence():
    """Show registered persistence classes."""
    show_unique(iter_persistence())

def show_persistence_schema(path_or_name):
    """Show persistence class schema.

    Parameters
    ----------
    path_or_name : str
        Proper python path or class name.
    """
    persistence = get_persistence(path_or_name)
    schema = persistence.get_schema()._schema.schema
    pprint(schema)
