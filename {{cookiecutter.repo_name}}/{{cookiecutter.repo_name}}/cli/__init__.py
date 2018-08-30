"""*{{ cookiecutter.repo_name | capitalize }}* command-line interface.

Command-line interface is implemented using `*Click* <http://click.pocoo.org/6/>`.

See Also
--------
click
"""
import os
import click
from {{ cookiecutter.repo_name }} import __name__
from .tasks import tasks
from .db import db
from .persistence import persistence
from .importers import importers

PACKAGE_NAME = __name__
CONTEXT_SETTINGS = {}

@click.group(context_settings=CONTEXT_SETTINGS)
@click.version_option(prog_name=PACKAGE_NAME.upper())
@click.option('--debug/--no-debug', default=False,
              help=f"Run '{PACKAGE_NAME}' in debug mode.")
def cli(debug):
    """{{ cookiecutter.repo_name | capitalize }} command-line interface.

    It is composed of several nested submodules, each of which is dedicated
    to different purposes such as task running, data import or general
    database management.
    """
    if debug:
        os.environ['LOGGING_LEVEL'] = 'DEBUG'
        click.echo(f"{PACKAGE_NAME.upper()}: running in DEBUG mode")


cli.add_command(tasks)
cli.add_command(db)
cli.add_command(persistence)
cli.add_command(importers)
