"""CLI: database management module."""
import click
from {{ cookiecutter.repo_name }}.cli.db.mongo import mongo
from {{ cookiecutter.repo_name }}.cli.db.dataimport import dataimport
from {{ cookiecutter.repo_name }}.cli.utils import eager_callback
from {{ cookiecutter.repo_name }}.cli.db.utils import show_db_connectors, show_db_models


@click.group()
@click.option('--show-dbs', is_flag=True, default=False, expose_value=False,
              is_eager=True, callback=eager_callback(show_db_connectors))
@click.option('--show-models', is_flag=True, default=False, expose_value=False,
              is_eager=True, callback=eager_callback(show_db_models))
def db():
    """Database management module."""
    pass


db.add_command(mongo)
db.add_command(dataimport)
