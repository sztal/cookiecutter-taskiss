"""CLI: DB submodule for MongoDB / Mongoengine management."""
import click
from {{ cookiecutter.repo_name }}.cli.utils import eager_callback
from {{ cookiecutter.repo_name }}.cli.db.utils import show_mongo_models, show_mongo_model_schema


@click.group()
@click.option('--show-models', is_flag=True, default=False, expose_value=False,
              is_eager=True, callback=eager_callback(show_mongo_models))
def mongo():
    """MongoDB / Mongoengine management inteface."""
    pass

@mongo.command(name='schema', help="Show schema of a MongoDB model.")
@click.argument('path_or_name', nargs=1, type=str)
def _(path_or_name):
    """Show schema of a MongoDB object.

    Main argument must be a proper python path or a simple class name.
    """
    show_mongo_model_schema(path_or_name)
