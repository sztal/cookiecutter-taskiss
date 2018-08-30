"""CLI: interface for managing persistence classes."""
import click
from ..utils import eager_callback
from .utils import show_persistence
from .utils import show_persistence_schema


@click.group()
@click.option('--show-classes', is_flag=True, default=False, expose_value=False,
              is_eager=True, callback=eager_callback(show_persistence))
def persistence():
    """Persistence classes management interface."""
    pass

@persistence.command(name='schema', help="Show schema of a persistence class.")
@click.argument('path_or_name', nargs=1, type=str)
def _(path_or_name):
    """Show schema of a persistence object.

    Main argument must be a proper python path or a simple class name.
    """
    show_persistence_schema(path_or_name)
