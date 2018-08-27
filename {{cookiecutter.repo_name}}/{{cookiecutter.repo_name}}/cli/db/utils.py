"""Utility functions for CLI database module."""
from {{ cookiecutter.repo_name }}.utils.app import iter_db_connectors, iter_db_models
from {{ cookiecutter.repo_name }}.cli.utils import pprint
from {{ cookiecutter.repo_name }}.base.abc import AbstractDBConnector


def show_db_connectors():
    """Get registered database connectors."""
    for conn in iter_db_connectors():
        pprint(conn)

def show_db_models():
    """Get registered database models."""
    for model in iter_db_models():
        pprint(model)
