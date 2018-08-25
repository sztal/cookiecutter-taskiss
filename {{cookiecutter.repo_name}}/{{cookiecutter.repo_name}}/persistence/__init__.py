"""Component classes for adding data persistence .

The aim is to inject persistence functionalities into classes
for data collection and/or long computations.
"""
# pylint: disable=W0613,W0221,W0212
import os
import json
from collections import deque
from logging import getLogger
from itertools import count
from smcore import get_persistence_path
from smcore.misc.path import make_filepath
from smcore.odm.utils import make_bulk_update, action_hook_set
from smcore.serializers import SmartJsonEncoder
from smcore.misc import safe_print


class Persistence(AttributeManagerMixin):
    """Abstract base persistence class.

    It defines the main persistence interface which is the `persist` method.
    """

    def __init__(self):
        """Initilization method."""
        self.counter = count(start=1)
        self.n_processed = None

    def persist(self, *args, **kwds):
        """Persist an object."""
        errmsg = "Class '{}' does not implement 'persist' interface.".format(
            self.__class__.__name__
        )
        raise NotImplementedError(errmsg)

    def get_counter(self, print_num=True, msg="\rProcessing item no. {} ..."):
        """Increment and get counter number.

        Parameters
        ----------
        print_num : bool
            Should number of processed items be printed.
        msg : str
            Formattable string with a message.
        """
        n = next(self.counter)
        self.n_processed = n
        if print_num and n > 1:
            safe_print(msg.format(n), nl=False)
        return n


class DiskPersistence(Persistence):
    """Disk persistence component class."""

    def __init__(self, filename=None, dirpath=None, **kwds):
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
        super().__init__()
        self._filepath = None
        self.filename = filename
        self.dirpath = \
            dirpath if dirpath else get_persistence_path(**kwds)

    @property
    def filepath(self):
        """str: Persistence filepath getter."""
        if not self._filepath:
            self._filepath = \
                make_filepath(self.filename, self.dirpath, inc_if_taken=True)
        return self._filepath


class JsonDiskPersistence(DiskPersistence):
    """JSON lines disk persitence component class.

    Attributes
    ----------
    filename : str
        Filename format string.
        Should have '{}' in place of persistence file number.
    dirpath : str
        Path to persistence storage directory.
    json_serializer : json.JSONEncoder
        `JSONEncoder` subclass defining JSON serializer.
        Defaults to `SmartJsonEncoder`.
    **kwds :
        Parameters passed to `get_persistence_path`.
    """

    def __init__(self, filename=None, dirpath=None,
                 json_serializer=SmartJsonEncoder, **kwds):
        """Initialization method."""
        super().__init__(filename, dirpath, **kwds)
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
            if print_num:
                self.get_counter(print_num=True)
            line = self.jsondump(doc)
            f.write(line+"\n")

    def jsondump(self, obj):
        """Dump an object to JSON string.

        This method handles date and datetime objects.

        Parameters
        ----------
        obj : any
            Any JSON-convertible object.
        """
        return json.dumps(obj, cls=self.json_serializer)


class MongoPersistence(Persistence):
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
                 action_hook=action_hook_set, logger=True):
        """Initialization method."""
        super().__init__()
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
