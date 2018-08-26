"""Mongoengine collection mixins.

This module defines powerfull `BaseDocumentMixin` which enhances
standard *Mongoengine* model classes with methods that enable
easy adjusting input data to a given model schema.
"""
from mongoengine import Document
from {{ cookiecutter.repo_name }}.utils.processors import parse_date, parse_bool


class BaseDocumentMixin(object):
    """Base document class mixin providing helper methods."""
    _field_names_map = {}

    # Class methods -----------------------------------------------------------

    @classmethod
    def _get_processors_map(cls):
        """Processors map getter method."""
        return {
            'IntField': int,
            'BooleanField': parse_bool,
            'DateTimeField': parse_date
        }

    @classmethod
    def _get_field_names_map(cls):
        """Field names map getter method."""
        return getattr(cls, 'field_names_map', {})

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
    def getval(cls, obj, field, **kwds):
        """Get value from an object using a field definition.

        Parameters
        ----------
        obj : any
            Some kind of object.
        field : str
            Field name.
        **kwds :
            Additional params passed to the serializer method.
        """
        fdef = cls._get_field_def(field)
        serializer = cls._get_processors_map().get(fdef.__class__.__name__)
        val = obj.get(field)
        if val is None:
            aliases = cls._get_field_names_map().get(field, [])
            for alias in aliases:
                val = obj.get(alias)
                if val is not None:
                    break
        if serializer and val is not None:
            val = serializer(val, **kwds)
        return val

    @classmethod
    def from_dict(cls, dct, only_dict=False):
        """Dict-based class constructor skeleton method.

        Parameters
        ----------
        dct : dict-like
            Record.
        only_dict : bool
            Should only dictionary instead of
            the document class instance be returned.
        """
        doc = { k: cls.getval(dct, k) for k in cls._fields.keys() if k != '_id' }
        if only_dict:
            return doc
        return cls(**doc)

    def to_dict(self, dump_id=False):
        """Dump document object to a dict.

        Parameters
        ----------
        dump_id : bool
            Should `_id` be also dumped.
        """
        fields = [ f for f in self._fields.keys() ]
        if not dump_id:
            for i in [ 'id', '_id' ]:
                if i in fields:
                    fields.remove(i)
        dct = { f: getattr(self, f) for f in fields }
        return dct
