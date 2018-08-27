"""Taskiss task arguments validator classes."""
from {{ cookiecutter.repo_name }}.base.validators import BaseValidator


class TaskissValidator(BaseValidator):
    """Standard *Taskiss* task arguments validator.

    By default it purges unknown arguments.
    """
    def __init__(self, *args, purge_unknown=True, **kwds):
        """Initialization method.

        See Also
        --------
        cerberus.Validator : `Validator` class and its `__init__` method
        """
        super().__init__(*args, purge_unknown=purge_unknown, **kwds)
