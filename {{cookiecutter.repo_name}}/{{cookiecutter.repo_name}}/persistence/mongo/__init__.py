"""*MongoDB* connector based on *pymongo* and *Mongoengine*

See Also
--------
pymongo
mongoengine
"""
import os
import time
from collections import Iterable
from pymongo import UpdateOne, UpdateMany
import mongoengine
from {{ cookiecutter.repo_name }}.persistence.mongo.utils import update_action_hook, query_factory
from {{ cookiecutter.repo_name }}.persistence import DBPersistence
from {{ cookiecutter.repo_name }}.base.interface import DBPersistenceInterface
from {{ cookiecutter.repo_name }}.base.validators import BaseValidator


def init(user, password, host, port, db, authentication_db=None, use_envvars=True):
    """Initilize Mongoengine ODM.

    Parameters
    ----------
    user : str
        Username to authenticate with.
    password : str
        User authentication password.
    host : str
        Host IP address/name.
    port : str
        Port number.
    db : str
        Database name.
    authentication_db : str or None
        Authentication databse name.
        Use `db` if `None`.
    """
    mongo_uri = 'mongodb://{username}:{password}@{host}:{port}/{db}'
    if not authentication_db:
        authentication_db = db
    uri = mongo_uri.format(
        username=user,
        password=password,
        host=host,
        port=port,
        db=db
    )
    mdb = mongoengine.connect(host=uri, authentication_source=authentication_db)
    return mdb


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
        :py:class:`{{ cookiecutter.repo_name }}.base.interface.DBPersistencInterface`.
    """
    _schema = BaseValidator({
        **DBPersistenceInterface._schema.schema,
        'model': { 'type': 'mongoengine_model' },
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


class MongoPersistence(DBPersistence):
    """MongoDB persistence class.

    See Also
    --------
    mongoengine
    """
    def __init__(self, settings=None, item_name='document', **kwds):
        """Initialization method.

        Parameters
        ----------
        settings : :py:class:`{{ cookiecutter.repo_name }}.persistence.mongo.MongoPersistenceInterface`
            MongoDB persistence settings object.
        item_name : str
            Item name
        **kwds :
            Other arguments passed to
            :py:class:`{{ cookiecutter.repo_name }}.persistence.mongo.MongoPersistenceInteface`
            when `settings=None`.
        """
        if not settings:
            settings = MongoPersistenceInterface(**kwds)
        super().__init__(settings, item_name)

    def persist(self, doc, print_num=True, **kwds):
        """Persist documents in MongoDB in batches.

        Parameters
        ----------
        doc : dict-like
            Dict-like object representing a valid MongoDB document.
        print_num : bool
            Should number of processed items be printed.
        **kwds :
            Parameters passed to `update`.
        """
        self.inc(print_num=print_num)
        if hasattr(self.model, 'from_dict'):
            doc = self.model.from_dict(doc, only_dict=True)
        self.queue.appendleft(doc)
        self.do_update(**kwds)

    def finalize(self):
        """Update last batch regardless of the size."""
        self.do_update(min_batch_size=0)

    def make_update_op(self, doc, multiple=None, upsert=None, **kwds):
        """Make :py:module:`pymongo` update op.

        Parameters
        ----------
        doc : Mapping
            Document to update.
        multiple : bool
            Should :py:class:`UpdateOne` or :py:class:`UpdateMany` be used.
        upsert : bool
            Should upsert mode be used instead of update.
        **kwds :
            Other arguments passed to :py:class:`UpdateOne` or :py:class:`UpdateMany`.
        """
        if multiple is None:
            multiple = self.multiple
        if upsert is None:
            upsert = self.upsert
        update_query = self.query(doc)
        update = self.processor(doc)
        if multiple:
            op = UpdateMany(update_query, update, upsert=upsert, **kwds)
        else:
            op = UpdateOne(update_query, update, upsert=upsert, **kwds)
        return op

    def make_bulk_update(self, bulk_write_kwds=None, **kwds):
        """Make bulk update.

        Parameters
        ----------
        bulk_write_kwds : dict or None
            Arguments passed to :py:function:`pymongo.bulk_write`.
            If `None` then `ordered=False` is passed.
        **kwds :
            Other arguments passed to
            :py:meth:`{{ cookiecutter.repo_name }}.persistence.mongo.MongoPersistence.make_update.op`.
        """
        if bulk_write_kwds is None:
            bulk_write_kwds = { 'ordered': False }
        bulk_ops = []
        while self.queue:
            op = self.make_update_op(self.queue.pop(), **kwds)
            bulk_ops.append(op)
        if bulk_ops:
            self.model._get_collection().bulk_write(bulk_ops, **bulk_write_kwds)

    def log_update_error(self, n_retry, exc, collection_name):
        """Log update error.

        Parameters
        ----------
        n_retry : int
            Number of retry that was made.
        exc : Exception
            Exception object.
        collection_name : str
            Collection name.
        """
        if not self.n_retry or self.n_retry < 0:
            errmsg = f"Failed to update collection '{collection_name}'"
            self.log(errmsg, method='exception', exc_info=exc)
        else:
            n_retry_left = self.n_retry - n_retry
            if n_retry == 0:
                errmsg = "Update for collection '{}' failed {} times. Stop retrying.".format(
                    collection_name, self.n_retry
                )
                self.log(errmsg, method='exception', exc_info=exc)
            else:
                errmsg = "Update for collection '{}' failed {} times. Retrying {} times.".format(
                    collection_name, n_retry, n_retry_left
                )
                self.log(errmsg, method='exception', exc_info=exc)


    def do_update(self, min_batch_size=None, update=None, **kwds):
        """Persist a batch of documents in MongoDB.

        Parameters
        ----------
        min_batch_size : int or None
            Minimal batch size.
            No minimal size if non-positive.
            Use configuration value if `None`.
        update : bool
            Should update mode be used instead of insert.
        **kwds :
            Parameters passed to `make_bulk_update`.

        Returns
        -------
        bool
            True if successful update has been done.
        """
        if update is None:
            update = self.update
        collection_name = self.model._get_collection_name()
        # Check if update should be done considering selected batch size
        if min_batch_size is None:
            if not self.batch_size or self.batch_size <= 0:
                min_batch_size = len(self.queue)
            else:
                min_batch_size = self.batch_size
        elif min_batch_size <= 0:
            min_batch_size = len(self.queue)
        if len(self.queue) < min_batch_size:
            return False
        # Perform update
        if not update:
            docs = [ self.model(**self.queue.pop()) for _ in range(len(self.queue)) ]
            self.model.objects.insert(docs)
        else:
            try:
                self.make_bulk_update(**kwds)
            except Exception as exc:
                if not self.n_retry or self.n_retry < 0:
                    self.log_update_error(-1, exc, collection_name)
                    raise exc
                n_retry = 0

    def get_model_name(self):
        """Get collection model name."""
        self.model._get_collection_name()

    def drop_model_data(self, query):
        """Drop model data.

        Parameters
        ----------
        query : dict
            Dict representing raw MongoDB query.
        """
        self.model.objects(__raw__=query).delete()
