"""Taskiss task arguments validator classes."""
# pylint: disable=W0235
from collections.abc import Callable
from collections import Iterable, Sequence, Mapping
from logging import Logger
from cerberus import Validator, TypeDefinition


class TaskissValidator(Validator):
    """Standard *Taskiss* task arguments validator.

    By default it purges unknown arguments.
    """
    types_mapping = Validator.types_mapping.copy()
    types_mapping['callable'] = TypeDefinition('callable', (Callable,), ())
    types_mapping['logger'] = TypeDefinition('logger', (Logger,), ())
    types_mapping['iterable'] = TypeDefinition('iterable', (Iterable), ())
    types_mapping['sequence'] = TypeDefinition('sequence', (Sequence,), ())
    types_mapping['mapping'] = TypeDefinition('mapping', (Mapping,), ())

    def __init__(self, *args, purge_unknown=True, **kwds):
        """Initialization method.

        See Also
        --------
        cerberus.Validator : `Validator` class and its `__init__` method
        """
        super().__init__(*args, purge_unknown=purge_unknown, **kwds)
