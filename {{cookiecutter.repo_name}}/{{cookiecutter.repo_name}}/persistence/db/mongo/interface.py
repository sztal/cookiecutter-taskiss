"""Mongo persistence interface."""
from {{ cookiecutter.repo_name }}.persistence.db.mongo.utils import query_factory, update_action_hook
from {{ cookiecutter.repo_name }}.base.interface import DBPersistenceInterface
from {{ cookiecutter.repo_name }}.base.validators import BaseValidator
from {{ cookiecutter.repo_name }}.utils.fetch import get_db_model


class MongoPersistenceInterface(DBPersistenceInterface):
    """Mongo persistence settings interface class.

    model : a database connection or model
        Any kind of connector / connection / model object.
    query : str or iterable of str or callable
        If callable, then it will be used on documents to generate update queries.
        If `str` or iterable of `str` then this fields will be used
        to lookup values in update query.
    processor : callable or None
        Optional callable to evaluate over all individual records (like map).
    update : bool
        Should update or insert mode be used for updating.
    upsert : bool
        Should upsert be used in update mode.
    multiple : bool
        Should multiple updates be used in update mode.
    **kwds :
        Other arguments passed to
        :py:class:`{{ cookiecutter.repo_name }}.base.interface.DBPersistenceInterface`.
    """
    _schema = BaseValidator({
        **DBPersistenceInterface._schema.schema,
        'model': {
            'type': 'mongoengine_model',
            'coerce': lambda x: get_db_model(x) if isinstance(x, str) else x,
        },
        'query': { 'type': 'callable', 'coerce': query_factory },
        'processor': {
            'type': 'callable',
            'nullable': True,
            'default': update_action_hook
        },
        'update': { 'type': 'boolean', 'default': True },
        'upsert': { 'type': 'boolean', 'default': True },
        'multiple': { 'type': 'boolean', 'default': False }
    })

    def __init__(self, **kwds):
        """Initialization method."""
        super().__init__(**kwds)
