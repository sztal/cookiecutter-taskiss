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
from {{ cookiecutter.repo_name }}.utils import safe_print
from {{ cookiecutter.repo_name }}.cli.utils import eager_callback, to_console

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

# @click.option('--graph', is_flag=True, default=False, expose_value=False, is_eager=True,
#               callback=eager_callback(lambda: ts.scheduler.show_dependency_graph()))
@tasks.command(name='stats', help="Show Celery stats.")
def _(): to_console(ts.scheduler.inspector.stats())
@tasks.command(name='report', help="Show Celery inspector report.")
def _(): to_console(ts.scheduler.inspector.report())
@tasks.command(name='ping', help="Ping Celery process.")
def _(): to_console(ts.scheduler.inspector.ping())
@tasks.command(name='active-queues', help="Show active Celery queues.")
def _(): to_console(ts.scheduler.inspector.active_queues())
@tasks.command(name='registered', help="Show registered tasks.")
def _(): to_console(ts.scheduler.get_registered_tasks())
@tasks.command(name='active', help="Show active tasks.")
def _(): to_console(ts.scheduler.inspector.active())
@tasks.command(name='scheduled', help="Show scheduled tasks.")
def _(): to_console(ts.scheduler.inspector.scheduled())
@tasks.command(name='reserved', help="Show reverved tasks.")
def _(): to_console(ts.scheduler.inspector.reserved())
@tasks.command(name='revoked', help="Show revoked tasks.")
def _(): to_console(ts.scheduler.inspector.revoked())
@tasks.command(name='conf', help="Get Celery configuration.")
def _(): to_console(ts.scheduler.inspector.conf())
@tasks.command(name='query-tasks', help="Query tasks by id.")
@click.argument('ids', nargs=-1, type=str)
def _(ids):
    to_console(ts.scheduler.inspector.query_task(*ids))
@tasks.command(name='graph', help="Show dependency graph.")
@click.argument('task', nargs=1, type=str, required=False)
@click.option('--labels/--no-labels', default=True,
              help="Should task labels be shown on the graph.")
def _(task, labels):
    """Show tasks dependency graph.

    Optional [TASK] (task name) subsets the graph
    only to the task dependent on it.

    Dependency graph shows relations between graph.
    Arrow pointing from the task to another shows that the second task
    depends on the first. This means that in some cases it should be
    automatically run after its dependencies are executed.
    """
    task = ts.scheduler.resolve_task_name(task)
    ts.scheduler.show_dependency_graph(task, with_labels=labels)
