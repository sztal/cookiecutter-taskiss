"""CLI: database management module."""
import click
from {{ cookiecutter.repo_name }}.cli.db.mongo import mongo


@click.group()
def db():
    """Database management module."""
    pass


db.add_command(mongo)
