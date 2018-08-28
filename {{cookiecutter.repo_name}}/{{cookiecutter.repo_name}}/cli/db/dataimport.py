"""CLI: DB submodule for importing data."""
import click
from {{ cookiecutter.repo_name }}.cli.utils import eager_callback
from {{ cookiecutter.repo_name }}.cli.db.utils import show_db_importers, show_db_importer_schema


@click.group()
@click.option('--show-importers', is_flag=True, default=False, expose_value=False,
              is_eager=True, callback=eager_callback(show_db_importers))
def dataimport():
    """Interface for importing data to databases."""
    pass

@dataimport.command(name='schema', help="Show schema of a database importer class")
@click.argument('path_or_name', nargs=1, type=str)
def _(path_or_name):
    """Show schema of a database importer class.

    Main must be a proper python path or a simple class name.
    """
    show_db_importer_schema(path_or_name)
