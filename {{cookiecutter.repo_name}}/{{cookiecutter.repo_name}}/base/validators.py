"""Base validator classes."""
from collections.abc import Callable
from logging import Logger
from mongoengine.base import BaseDocument, DocumentMetaclass, TopLevelDocumentMetaclass
from cerberus import Validator, TypeDefinition


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

    def __init__(self, *args, allow_unknown=False, purge_unknown=False, **kwds):
        """Initialization method."""
        kwds.update(allow_unknown=allow_unknown, purge_unknown=purge_unknown)
        super().__init__(*args, **kwds)
