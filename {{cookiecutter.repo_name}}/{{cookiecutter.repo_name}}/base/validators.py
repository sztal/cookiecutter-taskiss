"""Base validator classes."""
from collections.abc import Callable
from collections import Iterable, Sequence, Mapping
from logging import Logger
from mongoengine.base import BaseDocument, DocumentMetaclass, TopLevelDocumentMetaclass
from cerberus import Validator, TypeDefinition
from {{ cookiecutter.repo_name }}.utils import is_python_path


def copy_schema(schema):
    """Copy schema definition."""
    if isinstance(schema, Validator):
        schema = schema.schema
    return dict(schema.copy())


class BaseValidator(Validator):
    """Base validator extends standard *Cerberos* validator with more types."""
    types_mapping = Validator.types_mapping.copy()
    types_mapping['callable'] = TypeDefinition('callable', (Callable,), ())
    types_mapping['logger'] = TypeDefinition('logger', (Logger,), ())
    types_mapping['mongoengine_model'] = \
        TypeDefinition('mongoengine_model', (
            BaseDocument,
            DocumentMetaclass,
            TopLevelDocumentMetaclass
        ), ())
    types_mapping['iterable'] = TypeDefinition('iterable', (Iterable), ())
    types_mapping['sequence'] = TypeDefinition('sequence', (Sequence,), ())
    types_mapping['mapping'] = TypeDefinition('mapping', (Mapping,), ())

    def __init__(self, *args, allow_unknown=False, purge_unknown=True, **kwds):
        """Initialization method.

        See Also
        --------
        cerberus.Validator : `Validator` class and its `__init__` method
        """
        kwds.update(allow_unknown=allow_unknown, purge_unknown=purge_unknown)
        super().__init__(*args, **kwds)

    def _validate_objectpath(self, path_or_name, field, value):
        """Test if a value is a python object path or class name.

        The rule's arguments are validated against this schema:
        {'type': 'boolean'}
        """
        if objectpath and not is_python_path(value, object_only=True):
            self._error(field, "Must be a proper python object path")


class DBImporterValidator(BaseValidator):
    """Database importer schema validator."""
    def __init__(self, *args, allow_unknown=False, purge_unknown=True, **kwds):
        """Initialization method.

        See Also
        --------
        cerberus.Validator : `Validator` class and its `__init__` method
        """
        kwds.update(allow_unknown=allow_unknown, purge_unknown=purge_unknown)
        super().__init__(*args, **kwds)
