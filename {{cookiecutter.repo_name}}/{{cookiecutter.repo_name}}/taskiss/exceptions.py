"""_Taskiss_ exception classes."""
from networkx.algorithms import simple_cycles


class AmbiguousTaskArgumentsError(Exception):
    """Embiguous task arguments error class."""

    def __init__(self, ambiguous, *args, **kwds):
        """Initialization method.

        Parameters
        ----------
        ambiguous : dict
            Dict with keys and ambiguous values.
        """
        message = "Ambiguous task arguments for:\n\t{}".format(
            "\n\t".join([ "{} => {}".format(k, v) for k, v in ambiguous.items() ])
        )
        super().__init__(message, *args, **kwds)


class CircularDependenciesError(Exception):
    """Circular dependencies error class."""

    def __init__(self, dependency_graph, *args, **kwds):
        """Initialization method.

        Parameters
        ----------
        dependency_graph : :py:class:`networkx.DiGraph`
            Dependency graph object.
        """
        cycles = simple_cycles(dependency_graph)
        message = "circular dependencies: {}".format(
            "; ".join([ "=>".join(cycle) for cycle in cycles ])
        )
        super().__init__(message, *args, **kwds)


class NonExistentTaskDependencyError(Exception):
    """Non-existent task dependency error class."""

    def __init__(self, dependency, *args, **kwds):
        """Initialization method.

        Parameters
        ----------
        dependency : str
            Name of dependency.
        """
        message = "Non-existent dependency ('{}') specified".format(dependency)
        super().__init__(message, *args, **kwds)


class AmbiguousTaskNameError(Exception):
    """Ambiguous task name error class."""

    def __init__(self, task, candidates, *args, **kwds):
        """Initialization method.

        Parameters
        ----------
        task : str
            Task name, possibly only its last *n* components.
        candidates : list of str
            Matching candidate task names.
        """
        message = "Ambigous task name '{}', matches with: {}".format(
            task, ", ".join(map(str, candidates))
        )
        super().__init__(message, *args, **kwds)


class TaskNotRegisteredError(Exception):
    """Task not registered error class."""

    def __init__(self, task, *args, **kwds):
        """Initialization method.

        Parameters
        ----------
        task : str
            Task name, possibly only its last *n* components.
        """
        message = f"Task name '{task}' does not match any registered tasks"
        super().__init__(message, *args, **kwds)
