"""CLI: task runner (Taskiss) module."""
import click
from celery.result import AsyncResult
from {{ cookiecutter.repo_name }}.taskiss import taskiss as ts
from {{ cookiecutter.repo_name }}.utils import safe_print
from {{ cookiecutter.repo_name }}.cli.utils import to_console, parse_args


@click.group()
def tasks():
    """Interface for interacting with the task scheduler.
    It can be used to run tasks and check their status etc.
    """
    pass

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
    ts.scheduler.show_dependency_graph(task, with_labels=labels)

@tasks.command(name='run', help="Run a task.")
@click.argument('task', nargs=1, type=str, required=True)
@click.option('--recursive/--not-recursive', '-r', default=False,
              help="Should task execution propagate recursively to dependent tasks.")
@click.option('--timeout', '-t', type=int, default=5,
              help="Timeout value when getting async results once a task finished.")
@click.option('--wait', '-w', type=int, default=5,
              help="Number of seconds to wait after each run of the event loop.")
@click.option('--arg', '-a', type=str, multiple=True,
              help="Args passed to the task (i.e. -a x=10).")
@click.option('--evalarg', '-e', type=str, multiple=True,
              help="Literal evaluated args passed to the task (i.e. -e x=['a'])")
@click.option('--get', '-g', type=int, required=False,
              help="Wait for given time to evaluate async results of the root task.")
def _(task, recursive, timeout, wait, arg, evalarg, get):
    """Run task."""
    kwds = { **parse_args(*arg), **parse_args(*evalarg, eval_args=True)}
    queue = ts.scheduler.run_task(
        task=task,
        timeout=timeout,
        propagate=recursive,
        wait=wait,
        **kwds
    )
    root_task = next(queue)
    to_console(root_task.task_id)
    if get is not None:
        to_console(root_task.get(get))
    if recursive:
        for task in queue:
            to_console(task.task_id)
            if get is not None:
                to_console(task.get(get))

@tasks.command(name='schema', help="Show task schema.")
@click.argument('task', nargs=1, type=str, required=True)
def _(task):
    """Show task schema that specifies its arguments."""
    task = ts.scheduler.get_task(task)
    to_console(task.interface.schema)
