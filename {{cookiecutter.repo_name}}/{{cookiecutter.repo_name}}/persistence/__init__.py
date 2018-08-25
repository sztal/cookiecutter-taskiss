"""Component classes for adding data persistence .

The aim is to inject persistence functionalities into classes
for data collection and/or long computations.
"""
# pylint: disable=W0613,W0221,W0212
import os
import json
from collections import deque, namedtuple
from logging import getLogger
from itertools import count
from {{ cookiecutter.repo_name }} import get_persistence_path
from {{ cookiecutter.repo_name }}.utils.path import make_path, make_filepath
from {{ cookiecutter.repo_name }}.persistence.mongo.utils import make_bulk_update, action_hook_set
from {{ cookiecutter.repo_name }}.utils.serializers import JSONEncoder
from {{ cookiecutter.repo_name }}.utils import safe_print
from {{ cookiecutter.repo_name }}.persistence.abc import AbstractPersistence


ConfigPersistencePath = namedtuple('ConfigPersistencePath', ['persistence_path'])


class BasePersistence(AbstractPersistence):
    """Base persistence class.

    It defines the main persistence interface which is the `persist` method.

    Attributes
    ----------
    item_name : str
        Name of the items being processed.
    """
    def __init__(self, item_name='item'):
        """Initilization method."""
        self._counter = count(start=1)
        self._count = 0
        self._cfg = ConfigPersistencePath(get_persistence_path())
        self.item_name = item_name

    @property
    def count(self):
        """Count of processed items getter."""
        return self._count

    @property
    def cfg(self):
        """Get persistence config."""
        return self._cfg

    def persist(self):
        """Persist an object."""
        errmsg = "Class '{}' does not implement 'persist' method.".format(
            self.__class__.__name__
        )
        raise NotImplementedError(errmsg)

    def inc(self, print_num=True, item_name=None,
            msg="\rProcessing {item_name} no. {n}", **kwds):
        """Increment counter of processed items.

        Parameters
        ----------
        print_num : bool
            Should number of processed items be printed to *stdout*.
        item_name : str
            Optional item name to overwrite instance level configuration.
        msg : str
            Formattable string with a message.
            It needs to have at least two interpolated parts with named
            `item_name` and `n`. More named interpolated parts may be used
            adn they can be supplied via `**kwds`.
        **kwds :
            Optional keyword arguments used to format the message string.
        """
        item_name = item_name if item_name is None else self.item_name
        n = next(self._counter)
        self._count = n
        if print_num and n > 1:
            safe_print(msg.format(tem_name=item_name, n=n, **kwds))
        return n


class DiskPersistence(BasePersistence):
    """Disk persistence component class.

    This is a base class (does not define proper `persist` method)
    used as a core for concrete peristence classes that write to disk.
    """
    def __init__(self, filename, dirpath=None, item_name='item', **kwds):
        """Initialization method.

        Attributes
        ----------
        filename : str
            Filename format string.
            Should have '{}' in place of persistence file number.
        dirpath : str
            Path to persistence storage directory.
        **kwds :
            Parameters passed to `get_persistence_path`.
        """
        super().__init__(item_name)
        self._filepath = None
        self.filename = filename
        self.dirpath = dirpath if dirpath else self.cfg.persistence_path

    @property
    def filepath(self):
        """str: Persistence filepath getter."""
        if not self._filepath:
            self._filepath = make_path(
                make_filepath(self.filename, self.dirpath, inc_if_taken=True),
                create_dir=True
            )
        return self._filepath

    def dump(self, obj):
        """Dump item to disk."""
        errmsg = "Class '{}' does not implement 'dump' method.".format(
            self.__class__.__name__
        )
        raise NotImplementedError(errmsg)

    def load(self, data):
        """Load item from data saved to disk."""
        errmsg = "Class '{}' does not implement 'load' method.".format(
            self.__class__.__name__
        )
        raise NotImplementedError(errmsg)

    def load_persisted_data(self, filepath=None):
        """Load data persisted to disk.

        Parameters
        ----------
        filepath : str or None
            Filepath to read from.
            If `None` then defaults to the instance attribute.
        """
        errmsg = "Class '{}' does not implement 'load_persisted_data' method.".format(
            self.__class__.__name__
        )
        raise NotImplementedError(errmsg)


class JSONLinesPersistence(DiskPersistence):
    """JSON lines disk persitence component class."""
    def __init__(self, filename, dirpath=None, json_serializer=JSONEncoder,
                 item_name='item', **kwds):
        """Initialization method.

        Parameters
        ----------
        filename : str
            Filename format string.
            Should have '{}' in place of persistence file number.
        dirpath : str
            Path to persistence storage directory.
        json_serializer : json.JSONEncoder
            :py:class:`json.JSONEncoder` subclass defining JSON serializer.
            Defaults to
            :py:class:`{{ cookiecutter.repo_name }}.utils.serializers.JSONEncoder`.
        **kwds :
            Parameters passed to `get_persistence_path`.
        """
        super().__init__(filename, dirpath, item_name, **kwds)
        self.json_serializer = json_serializer

    def persist(self, doc, print_num=True):
        """Persist a json-formattable document.

        Parameters
        ----------
        doc : json-like
            Any object that can be dumped to a JSON string.
        print_num : bool
            Should number of processed documents be printed.
        """
        with open(self.filepath, 'a') as f:
            self.inc(print_num=print_num)
            line = self.dump(doc)
            f.write(line+"\n")

    def dump(self, obj):
        """Dump an object to JSON string.

        This method handles date and datetime objects.

        Parameters
        ----------
        obj : any
            Any JSON-convertible object.
        """
        return json.dumps(obj, cls=self.json_serializer)

    def load(self, data):
        """Load JSON object from string.

        Parameters
        ----------
        data : str
            JSON string.
        """
        return json.loads(data.strip())

    def load_persisted_data(self, filepath=None):
        """Load data persisted to disk.

        Parameters
        ----------
        filepath : str or None
            Filepath to read from.
            If `None` then defaults to the instance attribute.

        Yields
        ------
        dict
            Persisted items.
        """
        filepath = filepath if filepath else self.filepath
        with open(filepath, 'r') as f:
            for line in f:
                yield self.load(line)


class MongoPersistence(BasePersistence):
    """MongoDB persistence component class.

    Attributes
    ----------
    model : mongoengine.Document
        Mongoengine collection model class.
    query_fields : str or iterable of str
        List of field names to use for update query.
    batch_size : int
        Default batch size when making bulk updates.
        Nonpositive values mean that all documents are updated in one batch.
    action_hook : func
        Action hook function for creating MongoDB update statements
        in the case of update mode.
        Default to standard `$set` statement.
    logger : bool or str
        Should logger be used to log bulk updates.
        If `True` then the root logger is used.
        If `False` no logging.
        If it is a `str` then a logger of given name is used.
    """

    def __init__(self, model=None, query_fields=None, batch_size=10**4,
                 action_hook=action_hook_set, logger=True, item_name='document'):
        """Initialization method."""
        super().__init__(item_name)
        self.model = model
        self.query_fields = query_fields
        self.batch_size = batch_size
        self.action_hook = action_hook_set
        self.documents = deque()
        self.already_dropped_collection = False
        self.set_logger(logger)

    def set_logger(self, name=None):
        """Set logger object.

        Parameters
        ----------
        name : bool, str or None
            Name of the logger to set. Use root logger if `True`.
            Do not set any logger if `None`.
        """
        if name and isinstance(name, str):
            logger = getLogger(name)
        elif name:
            logger = getLogger()
        else:
            logger = None
        self.logger = logger

    def persist(self, doc=None, print_num=True, log=True, **kwds):
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
        if doc is not None:
            self.get_counter(print_num=print_num)
            if hasattr(self.model, 'from_dict'):
                doc = self.model.from_dict(doc, only_dict=True)
            self.documents.appendleft(doc)
        updated = self.update(**kwds)
        if updated and log:
            if print_num:
                safe_print("")
            self.logger.info("Updated collection '%s' [%d records in total]",
                             self.model._get_collection_name(), self.n_processed)

    def update(self, query_fields=None, min_batch_size=None,
               action_hook=None, update=True, drop_first=False, **kwds):
        """Persist a batch of documents in MongoDB.

        Parameters
        ----------
        documents : list-like of dict-like objects
            A list-like of dict-like object representing a valid MongoDB document.
            Must provide `pop` method.
        query_fields : str or iterable of str
            Field names for update query.
            If `None` then instance attribute is used.
        min_batch_size : int
            Minimal batch size. Instance attribute is used if `None`.
        action_hook : func or None
            Function for transforming documents into proper MongoDB update actions.
            Use `action_hook_set` if `None`.
        update : bool
            Should update mode be used instead of insert.
        drop_first : bool
            Should collection be reset and dropped before updating
        **kwds :
            Parameters passed to `make_bulk_update`.

        Returns
        -------
        bool
            True if successful update has been done.
        """
        collname = self.model._get_collection_name()
        # Optionally drop existing data
        if drop_first and not self.already_dropped_collection:
            if self.logger:
                self.logger.info("Dropping collection '%s'", collname)
            self.model.drop_collection()
            self.already_dropped_collection = True
        # Check if update should be done considering selected batch size
        if min_batch_size is None:
            min_batch_size = self.batch_size
        elif min_batch_size <= 0:
            min_batch_size = len(self.documents)
        if len(self.documents) < min_batch_size:
            return False
        # Do the update
        if not query_fields:
            query_fields = self.query_fields
        # Perform update
        if not action_hook:
            action_hook = self.action_hook
        docs = [ self.documents.pop() for _ in range(min_batch_size) ]
        if not update:
            docs = [ self.model(**d) for d in docs ]
            self.model.objects.insert(docs)
        else:
            if not self.query_fields:
                errmsg = "Trying to do bulk update with undefined 'query_fields'"
                raise AttributeError(errmsg)
            make_bulk_update(
                data=docs,
                query_fields=query_fields,
                model=self.model,
                **kwds
            )
        # Return flag indicating successful update
        return True
