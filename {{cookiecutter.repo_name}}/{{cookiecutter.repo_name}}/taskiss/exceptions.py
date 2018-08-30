"""*Taskiss* exception classes."""
from networkx.algorithms import simple_cycles


class AmbiguousTaskArgumentsError(Exception):
    """Embiguous task arguments error class."""

    @classmethod
    def from_ambiguous(cls, ambiguous, *args, **kwds):
        """Dict-based constructor.

         Parameters
        ----------
        ambiguous : dict
            Dict with keys and ambiguous values.
        """
        message = "Ambiguous task arguments for:\n\t{}".format(
            "\n\t".join([ "{} => {}".format(k, v) for k, v in ambiguous.items() ])
        )
        return cls(message, *args, **kwds)


class CircularDependenciesError(Exception):
    """Circular dependencies error class."""

    @classmethod
    def from_dependency_graph(cls, dependency_graph, *args, **kwds):
        """Dependency graph based constructor.

        Parameters
        ----------
        dependency_graph : :py:class:`networkx.DiGraph`
            Dependency graph object.
        """
        cycles = simple_cycles(dependency_graph)
        message = "circular dependencies: {}".format(
            "; ".join([ "=>".join(cycle) for cycle in cycles ])
        )
        return cls(message, *args, **kwds)


class NonExistentTaskDependencyError(Exception):
    """Non-existent task dependency error class."""

    @classmethod
    def from_dependency(cls, dependency, *args, **kwds):
        """Dependency based constructor.

        Parameters
        ----------
        dependency : str
            Name of dependency.
        """
        message = "Non-existent dependency ('{}') specified".format(dependency)
        return cls(message, *args, **kwds)


class AmbiguousTaskNameError(Exception):
    """Ambiguous task name error class."""

    @classmethod
    def from_task(cls, task, candidates, *args, **kwds):
        """Task and candidates based constructor.

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
        return cls(message, *args, **kwds)


class TaskNotRegisteredError(Exception):
    """Task not registered error class."""

    @classmethod
    def from_task(cls, task, *args, **kwds):
        """Task based constructor.

        Parameters
        ----------
        task : str
            Task name, possibly only its last *n* components.
        """
        message = f"Task name '{task}' does not match any registered tasks"
        return cls(message, *args, **kwds)


class BadTaskArgumentsError(Exception):
    """Bad task arguments error class."""
    pass
