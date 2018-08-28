"""CLI: data importers module."""
import click
from {{ cookiecutter.repo_name }}.cli.utils import eager_callback, parse_args
from {{ cookiecutter.repo_name }}.cli.importers.utils import show_importers, show_importer_schema
from {{ cookiecutter.repo_name }}.cli.importers.utils import run_importer



@click.group()
@click.option('--show-importers', is_flag=True, default=False, expose_value=False,
              is_eager=True, callback=eager_callback(show_importers))
def importers():
    """Interface for importing data to databases."""
    pass

@importers.command(name='schema', help="Show schema of a database importer class")
@click.argument('path_or_name', nargs=1, type=str)
def _(path_or_name):
    """Show schema of a database importer class.

    Main must be a proper python path or a simple class name.
    """
    show_importer_schema(path_or_name)

@importers.command(name='import-data', help="Import data to a persistence storage.")
@click.argument('importer_path_or_name', nargs=1, type=str)
@click.argument('persistence_path_or_name', nargs=1, type=str)
@click.option('--arg', '-a', type=str, multiple=True,
              help="Args passed to importer and/or persistence (i.e. -a x=10).")
@click.option('--evalarg', '-e', type=str, multiple=True,
              help="Literal evaluated args passed to importer and/or persistence (i.e. -a x=['a']).")
def _(importer_path_or_name, persistence_path_or_name, arg, evalarg):
    """Run importer."""
    kwds = { **parse_args(*arg), **parse_args(*evalarg, eval_args=True) }
    run_importer(importer_path_or_name, persistence_path_or_name, log=True, **kwds)
