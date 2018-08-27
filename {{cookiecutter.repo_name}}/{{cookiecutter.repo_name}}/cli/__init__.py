"""*{{ cookiecutter.repo_name | capitalize }}* command-line interface.

Command-line interface is implemented using `*Click* <http://click.pocoo.org/6/>`.

See Also
--------
click
"""
import os
import click
import {{ cookiecutter.repo_name }}
from {{ cookiecutter.repo_name }}.taskiss import taskiss as ts
from {{ cookiecutter.repo_name }}.cli.utils import eager_callback

PACKAGE_NAME = {{ cookiecutter.repo_name }}.__name__
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

@cli.group()
def tasks():
    """Interface for interacting with the task scheduler.
    It can be used to run tasks and check their status etc.
    """
    pass

@tasks.command(name='list', help="Show registered tasks.")
@click.option('--graph', is_flag=True, default=False, expose_value=False, is_eager=True,
              callback=eager_callback(lambda: ts.scheduler.show_dependency_graph()))
def _():
    """Show registered tasks or display them in a form of a dependency graph."""
    for task in ts.scheduler.get_registered_tasks():
        click.echo(task)
