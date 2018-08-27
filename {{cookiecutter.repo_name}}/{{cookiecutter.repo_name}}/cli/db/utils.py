"""Utility functions for CLI database module."""
from {{ cookiecutter.repo_name }}.utils import iter_objects
from {{ cookiecutter.repo_name }}.cli.utils import pprint
from {{ cookiecutter.repo_name }}.base.abc import AbstractDBConnector


def show_db_connectors():
    """Get registered database connectors."""
    obj = iter_objects(
        path='.taskiss',
        obj_predicate=lambda x: isinstance(x, AbstractDBConnector),
    )
    for o in obj:
        pprint(o)
