"""CLI: DB submodule for importing data."""
import click
from {{ cookiecutter.repo_name }}.cli.utils import eager_callback
from {{ cookiecutter.repo_name }}.cli.db.utils import show_db_importers


@click.group()
@click.option('--show-importers', is_flag=True, default=False, expose_value=False,
              is_eager=True, callback=eager_callback(show_db_importers))
def dataimport():
    """Interface for importing data to databases."""
    pass
