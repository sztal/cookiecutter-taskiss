"""CLI: database management module."""
import click
from {{ cookiecutter.repo_name }}.cli.db.mongo import mongo
from {{ cookiecutter.repo_name }}.cli.utils import eager_callback
from {{ cookiecutter.repo_name }}.cli.db.utils import show_db_connectors


@click.group()
@click.option('--show-dbs', is_flag=True, default=False, expose_value=False, is_eager=True,
              callback=eager_callback(lambda: show_db_connectors()))
def db():
    """Database management module."""
    pass


db.add_command(mongo)
