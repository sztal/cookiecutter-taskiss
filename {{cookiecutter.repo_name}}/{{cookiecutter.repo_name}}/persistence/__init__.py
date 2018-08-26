"""Component classes for adding data persistence .

The aim is to inject persistence functionalities into classes
for data collection and/or long computations.

Attributes
----------
"""
# pylint: disable=W0613,W0221,W0212
import os
import json
from collections import deque
from logging import getLogger
from itertools import count
from {{ cookiecutter.repo_name }}.utils.path import get_persistence_path, make_path, make_filepath
from {{ cookiecutter.repo_name }}.utils.serializers import JSONEncoder
from {{ cookiecutter.repo_name }}.utils import safe_print
from {{ cookiecutter.repo_name }}.meta import Composable
from {{ cookiecutter.repo_name }}.persistence.cfg import DiskPersistenceConfig


class BasePersistence(metaclass=Composable):
    """Base persistence class.

    It defines the main persistence interface which is the `persist` method.

    Attributes
    ----------
    cfg : Mapping
        Persistsence config.
    item_name : str
        Name of the items being processed.
    """
    def __init__(self, cfg=None, item_name='item'):
        """Initilization method."""
        self.setcomponents([ ('_cfg', cfg) ])
        self._counter = count(start=1)
        self._count = 0
        self.item_name = item_name
        self.queue = deque()

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
            safe_print(msg.format(item_name=item_name, n=n, **kwds))
        return n

    def log(self, msg="Processed {n} {item_name}s"):
        """Log information about work done.

        Parameters
        ----------
        msg : str
            Message to log.
            Has to be a formattable string with placeholders `n` and `item_name`.
        """
        if self.logger and self.batch_size \
        and self.batch_size > 0 and self.count % self.batch_size == 0:
            self.logger.info(msg.format(n=self.count, item_name=self.item_name))

# Disk persistence classes ----------------------------------------------------

class DiskPersistence(BasePersistence):
    """Disk persistence component class.

    This is a base class (does not define proper `persist` method)
    used as a core for concrete peristence classes that write to disk.
    """
    def __init__(self, cfg=None, item_name='item'):
        """Initialization method.

        Parameters
        ----------
        cfg : :py:class:`{{ cookiecutter.repo_name }}.persistence.DiskPersistenceConfig`
            Disk persistence config providing the persistence directory path
            and the filename.
        item_name : str
            Item name.
        """
        super().__init__(cfg, item_name)
        self._filepath = None

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

    def __init__(self, cfg=None, json_serializer=JSONEncoder, item_name='item', **kwds):
        """Initialization method.

        Parameters
        ----------
        cfg : :py:class:`{{ cookiecutter.repo_name }}.persistence.DiskPersistenceConfig`
            Disk persistence config providing the persistence directory path
            and the filename.
            If `None` then an instance of `DiskPersistenceConfig`
            is created from `**kwds`.
        json_serializer : json.JSONEncoder
            :py:class:`json.JSONEncoder` subclass defining JSON serializer.
            Defaults to
            :py:class:`{{ cookiecutter.repo_name }}.utils.serializers.JSONEncoder`.
        item_name : str
            Item name.
        **kwds :
            Other arguments passed to
            :py:class:`{{ cookiecutter.repo_name }}.persistence.cfg.DiskPersistenceConfig`
            when `cfg` is `None`.
        """
        if not cfg:
            cfg = DiskPersistenceConfig(**kwds)
        super().__init__(cfg, item_name)
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


# Database persistence classes ------------------------------------------------

class DBPersistence(BasePersistence):
    """Database persistence base class."""

    def __init__(self, cfg, item_name='record'):
        """Initialization method.

        Parameters
        ----------
        cfg : :py:class:`{{ cookiecutter.repo_name }}.persistence.DBPersistenceConfig`
            Database persistence configuration.
        item_name : str
            Item name.
        """
        super().__init__(cfg, item_name)

    def __enter__(self):
        """Enter hook."""
        pass

    def __exit__(self, type, value, traceback):
        """Exit hook."""
        self.finalize()
