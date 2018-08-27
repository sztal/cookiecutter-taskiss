"""Utility functions for CLI database module."""
from {{ cookiecutter.repo_name }}.utils.app import iter_db_connectors
from {{ cookiecutter.repo_name }}.cli.utils import pprint
from {{ cookiecutter.repo_name }}.base.abc import AbstractDBConnector


def show_db_connectors():
    """Get registered database connectors."""
    for conn in iter_db_connectors():
        pprint(conn)
