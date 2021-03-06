"""Mongoengine collection mixins.

This module defines powerfull `BaseDocumentMixin` which enhances
standard *Mongoengine* model classes with methods that enable
easy adjusting input data to a given model schema.
"""
from mongoengine.base.fields import BaseField
from cerberus import Validator
from {{ cookiecutter.repo_name }}.utils.processors import parse_date, parse_bool
from {{ cookiecutter.repo_name }}.base.abc import AbstractDBMixin


BASESCHEMA = {
    'IntField': {
        'type': 'integer',
        'coerce': int
    },
    'BooleanField': {
        'type': 'boolean',
        'coerce': parse_bool
    },
    'DateTimeField': {
        'type': 'datetime',
        'coerce': parse_date
    },
    'FloatField': {
        'type': 'float',
        'coerce': float
    },
    'StringField': {
        'type': 'string',
        'coerce': str
    },
    'ListField': {
        'type': 'list',
        'coerce': list
    },
    'DictField': {
        'type': 'dict',
        'coerce': dict
    }
}

ATTRMAP = Validator({
    'required': {
        'type': 'boolean',
        'coerce': lambda x: not bool(x),
        'rename': 'nullable',
        'nullable': True
    },
    'default': { 'nullable': True },
    'choices': {
        'type': 'list',
        'rename': 'allowed',
        'nullable': True
    },
    'min': {
        'type': 'integer',
        'coerce': int,
        'nullable': True
    },
    'max': {
        'type': 'integer',
        'coerce': int,
        'nullable': True
    },
    'min_length': {
        'type': 'integer',
        'coerce': int,
        'nullable': True
    },
    'max_length': {
        'type': 'integer',
        'coerce': int,
        'nullable': True
    }
})


class BaseDocumentMixin:
    """Base document class mixin providing helper methods."""
    _field_names_map = {}
    _schema = None
    _ignore_fields = [ '_id', 'id' ]
    _baseschema = BASESCHEMA

    # Class methods and properties --------------------------------------------

    @classmethod
    def _get_fields_defs(cls, ignore_fields=True, *args):
        """Get fields definitions."""
        fields = cls._fields
        if ignore_fields:
            fields = {
                k: v for k, v in fields.items()
                if k not in [ *cls._ignore_fields, *args ]
            }
        return fields

    @classmethod
    def _get_field_def(cls, field):
        """Get field definition.

        Parameters
        ----------
        field : str
            Field name.
        """
        return cls._fields[field]

    @classmethod
    def _extract_attrs(cls, field):
        """Extract schema-related field attributes."""
        dct = { k: getattr(field, k, None) for k in ATTRMAP.schema }
        dct = ATTRMAP.normalized(dct)
        return { k: v for k, v in dct.items() if v }

    @classmethod
    def _extract_field_schema(cls, field_name, field):
        """Extract field schema from *Mongoengine* field object."""
        field_type = field.__class__.__name__
        _schema = cls._baseschema.get(field_type, {})
        _schema.update(**cls._extract_attrs(field))
        rename = cls._field_names_map.get(field_name, [])
        if rename and isinstance(rename, str):
            rename = [ rename ]
        if rename:
            for r in rename:
                schema = { r: { **_schema, 'rename': field_name } }
                yield schema
        else:
            yield { field_name: _schema }

    @classmethod
    def get_schema(cls, *args, **kwds):
        """Initialize (if needed) and get the schema object.

        Parameters
        ----------
        *args :
            Positional arguments passed to `_get_fields_defs` method.
        **kwds :
            Keyword arguments passed to `_get_fields_defs` method.
        """
        if not cls._schema:
            fields = cls._get_fields_defs(*args, **kwds)
            schema = {}
            for k, v in fields.items():
                field_schema = cls._extract_field_schema(k, v)
                for fs in field_schema:
                    schema = { **schema, **fs }
            cls._schema = Validator(schema, allow_unknown=False, purge_unknown=True)
        return cls._schema

    @classmethod
    def from_dict(cls, dct, only_dict=False, *args, **kwds):
        """Dict-based class constructor skeleton method.

        Parameters
        ----------
        dct : dict-like
            Record.
        only_dict : bool
            Should only dictionary instead of
            the document class instance be returned.
        *args :
            Positional arguments passed to `get_schema`.
        **kwds :
            Keyword arguments passed to `get_schema`.
        """
        schema = cls.get_schema(*args, **kwds)
        doc = schema.normalized(dct)
        if only_dict:
            return doc
        return cls(**doc)

    def to_dict(self, *args, ignore_fields=True, only=()):
        """Dump document object to a dict.

        Parameters
        ----------
        ignore_fields : bool
            Should fields be ignored.
            Ignored fields are defined in `_ignore_fields` class attribute
            and may be extended with additional `*args`.
        only : list of str
            Return only selected fields.
        """
        if only:
            fields = only
        else:
            ignore = getattr(self, '_ignore_fields', []) if ignore_fields else []
            ignore = [ *ignore, *args ]
            fields = [ f for f in self._fields if f not in ignore ]
        dct = { f: getattr(self, f) for f in fields }
        return dct


AbstractDBMixin.register(BaseDocumentMixin)
