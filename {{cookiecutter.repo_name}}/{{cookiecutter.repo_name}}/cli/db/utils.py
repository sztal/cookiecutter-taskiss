"""CLI: commands of the DB module."""
from {{ cookiecutter.repo_name }}.utils.fetch import iter_db_connectors, iter_db_models
from ..utils import to_console
from ..utils import show_unique


def show_db_connectors():
    """Show registered database connectors."""
    show_unique(iter_db_connectors())

def show_db_models():
    """Show registered database models."""
    show_unique(iter_db_models())
