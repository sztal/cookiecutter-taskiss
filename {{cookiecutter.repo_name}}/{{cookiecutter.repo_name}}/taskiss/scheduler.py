"""Scheduler for controlling execution of _Celery_ tasks.

One of the main functionalities of this class is to take care of explicit
dependencies declared between tasks, so execution of parent task can properly
trigger subsequent execution of all children tasks, when needed.

Dependencies are encoded as a dependency graph, structured as a simple `dict`.
Circular dependencies needs to be avoided at all costs and will be detected
every time the dependency graph is (re)built.
"""
import time
from collections import defaultdict
from importlib import import_module
from celery import Task
from celery.result import ResultSet
from celery.task.control import inspect
from networkx import DiGraph, draw_shell
from networkx.algorithms import is_directed_acyclic_graph, simple_cycles
from networkx.algorithms import descendants, topological_sort
import matplotlib.pyplot as pyplot
from {{ cookiecutter.repo_name }}.taskiss.utils import merge_results
from {{ cookiecutter.repo_name }}.taskiss.exceptions import CircularDependenciesError
from {{ cookiecutter.repo_name }}.taskiss.exceptions import NonExistentTaskDependencyError
from {{ cookiecutter.repo_name }}.taskiss.exceptions import AmbiguousTaskNameError
from {{ cookiecutter.repo_name }}.taskiss.exceptions import TaskNotRegisteredError


class Scheduler(object):
    """Celery task scheduler.

    Attributes
    ----------
    dependency_graph : :py:class:`networkx.classes.digraph.DiGraph`
        Dependency graph.
    """
    def __init__(self, include, build_dependency_graph=True, **kwds):
        """Initialization method.

        Parameters
        ----------
        include : list of str
            List of python module paths pointing to task modules.
        build_dependency_graph : bool
            Should dependency graph be built during the initialization.
            Setting to `False` may be useful for testing etc.
        **kwds :
            Other params passed to :py:meth:`.Scheduler.build_dependency_graph`.
        """
        self.include = include
        if build_dependency_graph:
            self.build_dependency_graph(**kwds)
        else:
            self.dependency_graph = DiGraph()

    @property
    def inspector(self):
        """Celery inspector getter."""
        return inspect()

    def get_registered_tasks(self, only_names=True):
        """Get list of registered Celery tasks.

        Parameters
        ----------
        only_names : bool
            Should only names instead of full task objects be returned.
        """
        tasks = []
        for module_name in self.include:
            m = import_module(module_name)
            for name in dir(m):
                if name.startswith('_'):
                    continue
                obj = getattr(m, name)
                if isinstance(obj, Task) and obj.name not in tasks:
                    task = obj.name if only_names else obj
                    tasks.append(task)
        return tasks

    def resolve_task_name(self, task):
        """Resolve shortened task name.

        Parameters
        ----------
        task : str
            Task name, possibly only its last *n* components.
        """
        tasks = self.get_registered_tasks(only_names=True)
        candidates = []
        task_parts = task.split('.')
        task_n = len(task_parts)
        for t in tasks:
            t_parts = t.split('.')
            t_n = len(t_parts)
            if t_n < task_n:
                continue
            tn = '.'.join(t_parts[-task_n:])
            if tn == task:
                candidates.append(t)
        if len(candidates) == 1:
            return candidates.pop()
        elif len(candidates) > 1:
            raise AmbiguousTaskNameError(task, candidates)
        raise TaskNotRegisteredError(task)

    def get_task(self, task_name):
        """Get task by name.

        Parameters
        ----------
        task_name : str
            Valid task name with full python module path.
        """
        try:
            task = import_module(task_name)
        except ModuleNotFoundError:
            task_name = task_name.split('.')
            tail = '.'.join(task_name[:-1])
            head = task_name[-1]
            task = getattr(import_module(tail), head)
        return task

    def register_task(self, task, check_cycles=True):
        """Register task and rebuild the dependency graph.

        Parameters
        ----------
        task : celery.Task
            Task object inheriting from :py:class:`celery.Task`.
            If `task` inherits from :py:class:`{{ cookiecutter.repo_name }}.DependentTask`
        check_cycles : bool
            Check if dependency graph is cyclic.

        Raises
        ------
        TypeError
            If `task` is not a subclass of :py:class:`celery.Task`.
        CircularDependenciesError
            If `check_cycles` is `True` and the graph is cyclic.
        """
        if isinstance(task, Task):
            self.dependency_graph.add_node(task.name)
            self._add_task_dependencies(task)
            if check_cycles and self.circular_dependencies():
                raise CircularDependenciesError(self.dependency_graph)
        else:
            raise TypeError("'task' must be a valid Celery task object")

    def circular_dependencies(self):
        """Check if there are circular dependencies."""
        return not is_directed_acyclic_graph(self.dependency_graph)

    def _add_task_dependencies(self, task):
        """Add task dependencies as edges in the graph."""
        all_tasks = self.get_registered_tasks()
        task = self.get_task(task)
        dependencies = getattr(task, 'dependson', None)
        if not dependencies:
            return
        for dep in dependencies:
            if dep not in all_tasks:
                raise NonExistentTaskDependencyError(dep)
            if dep not in self.dependency_graph.nodes:
                self.dependency_graph.add_node(dep)
        edges = [ (dep, task.name) for dep in dependencies ]
        if edges:
            self.dependency_graph.add_edges_from(edges)

    def build_dependency_graph(self, check_cycles=True):
        """(Re)build dependency graph.

        Parameters
        ----------
        check_cycles : bool
            Check if dependency graph is cyclic.

        Raises
        ------
        CircularDependenciesError
            If `check_cycles` is `True` and the graph is cyclic.
        """
        self.dependency_graph = DiGraph()
        tasklist = self.get_registered_tasks()
        self.dependency_graph.add_nodes_from(tasklist)
        for task in tasklist:
            self._add_task_dependencies(task)
        if check_cycles and self.circular_dependencies():
            raise CircularDependenciesError(self.dependency_graph)

    def show_dependency_graph(self, task=None, with_labels=True, **kwds):
        """Show dependency graph.

        Parameters
        ----------
        task : str
            Optional task name.
            If specified then only a subgraph starting from the task
            considered as the root node is showed.
        with_labels : bool
            Should labels be shown on the graph.
        **kwds :
            Other params passed to :py:function:`networkx.draw`.
        """
        graph = self.dependency_graph
        if task:
            graph = graph.subgraph([ task, *descendants(graph, task)])
        draw_shell(graph, with_labels=with_labels, **kwds)
        pyplot.show()

    def get_ordered_descendants(self, task):
        """Get descendants of task ordered using topological sort.

        Parameters
        ----------
        task : str
            Task name.
        """
        toposort = topological_sort(self.dependency_graph)
        dependent_tasks = [
            t for t in toposort
            if t in descendants(self.dependency_graph, task)
        ]
        return dependent_tasks

    def run_task(self, task, timeout=5, propagate=False, wait=5, **kwds):
        """Run task.

        This function runs a Celery task and optionally
        propagates execution down to all tasks below on the dependency graph.

        Parameters
        ----------
        task : str or celery.Task
            Task object or task name.
        timeout : int
            Timeout value used when fetching async results.
        propagate : bool
            Should changes be propagated down the dependency graph.
        wait : float or int
            Wait time between subsequent loops in the 'event loop'.
        **kwds :
            Keyword arguments passed to the top task.
        """
        if isinstance(task, str):
            task = self.get_task(task)
        tasksort = self.get_ordered_descendants(task.name)
        graph = self.dependency_graph.subgraph([ task.name, *tasksort ])
        taskdct = defaultdict(lambda: None)
        taskdct[task.name] = task.delay(**kwds)
        yield taskdct[task.name]
        if not propagate:
            return

        def run_next_tasks(tasksort):
            """Inner loop for running subsequent tasks."""
            finished = set()
            for next_task in tasksort:
                deps = list(graph.predecessors(next_task))
                rset = ResultSet([])
                for dep in deps:
                    toptask = taskdct[dep]
                    if toptask:
                        rset.add(toptask)
                if rset.successful() and rset.completed_count() == len(deps):
                    kwds = merge_results(*rset.join(timeout=timeout))
                    next_result = self.get_task(next_task).delay(**kwds)
                    taskdct[next_task] = next_result
                    finished.add(next_task)
                    yield next_result
                elif rset.failed():
                    # TODO: add proper handling of failed tasks
                    finished.add(next_task)
                    for child in graph.successors(next_task):
                        finished.add(child)
            yield from finished

        while tasksort:
            time.sleep(wait)
            for item in run_next_tasks(tasksort):
                if isinstance(item, str) and item in tasksort:
                    tasksort.remove(item)
                else:
                    yield item
