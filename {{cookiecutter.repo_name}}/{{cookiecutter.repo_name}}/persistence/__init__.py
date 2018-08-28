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
from {{ cookiecutter.repo_name }}.utils.app import get_persistence_path
from {{ cookiecutter.repo_name }}.utils.path import make_path, make_filepath
from {{ cookiecutter.repo_name }}.utils.serializers import JSONEncoder
from {{ cookiecutter.repo_name }}.utils import safe_print
from {{ cookiecutter.repo_name }}.base.meta import Composable
from {{ cookiecutter.repo_name }}.base.interface import DiskPersistenceInterface, DBPersistenceInterface
from {{ cookiecutter.repo_name }}.base.validators import BaseValidator
from {{ cookiecutter.repo_name }}.base.abc import AbstractPersistenceMetaclass


class AbstractComposablePersistenceMetaclass(AbstractPersistenceMetaclass, Composable):
    """Composable persistence abstract metaclass."""
    pass


class BasePersistence(metaclass=AbstractComposablePersistenceMetaclass):
    """Base persistence class.

    It defines the main persistence interface which is the `persist` method.

    Attributes
    ----------
    settings : object
        Persistence settings.
    item_name : str
        Name of the items being processed.
    """
    _interface = None

    def __init__(self, item_name='item', **kwds):
        """Initilization method.

        Parameters
        ----------
        item_name : str
            Item name.
        **kwds :
            Keyword arguments passed to the constructor of the
            settings interface.
        """
        settings = self.interface(**kwds)
        self.setcomponents_([ ('settings', settings) ])
        self._counter = count(start=1)
        self._count = 0
        self.item_name = item_name
        self.queue = deque()

    def __enter__(self):
        """Enter hook."""
        self.prepare()

    def __exit__(self, type, value, traceback):
        """Exit hook."""
        self.finalize()

    @property
    def interface(self):
        """Interface getter."""
        if not self._interface:
            cn = self.__class__.__name__
            raise AttributeError(f"'{cn}' does not define interface")
        return self._interface

    @property
    def count(self):
        """Count of processed items getter."""
        return self._count

    def finalize(self):
        """Finalize update."""
        pass

    def prepare(self):
        """Prepare update."""
        pass

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
        item_name = item_name if item_name else self.item_name
        n = next(self._counter)
        self._count = n
        if print_num and n > 1:
            safe_print(msg.format(item_name=item_name, n=n, **kwds), nl=False)
        return n

# Disk persistence classes ----------------------------------------------------

class DiskPersistence(BasePersistence):
    """Disk persistence component class.

    This is a base class (does not define proper `persist` method)
    used as a core for concrete peristence classes that write to disk.
    """
    _interface = DiskPersistenceInterface

    def __init__(self, item_name='item', **kwds):
        """Initialization method.

        Parameters
        ----------
        item_name : str
            Item name.
        **kwds :
            Settings passed to `DiskPersistenceSettings` constructor
        """
        super().__init__(item_name, **kwds)
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

    def __init__(self, json_serializer=JSONEncoder, item_name='item', **kwds):
        """Initialization method.

        Parameters
        ----------
        json_serializer : json.JSONEncoder
            :py:class:`json.JSONEncoder` subclass defining JSON serializer.
            Defaults to
            :py:class:`{{ cookiecutter.repo_name }}.utils.serializers.JSONEncoder`.
        item_name : str
            Item name.
        **kwds :
            Other arguments passed to
            :py:class:`{{ cookiecutter.repo_name }}.base.interface.DiskPersistenceInteface`
            when `settings=None`.
        """
        super().__init__(item_name, **kwds)
        self.json_serializer = json_serializer

    def persist(self, doc, print_num=True, **kwds):
        """Persist a json-formattable document.

        Parameters
        ----------
        doc : json-like
            Any object that can be dumped to a JSON string.
        print_num : bool
            Should number of processed documents be printed.
        **kwds :
            Keyword arguments passed to
            :py:meth:`{{ cookiecutter.repo_name }}.persistence.DiskPersistence.log_progress`.
        """
        batch_size = getattr(self, 'batch_size', None)
        with open(self.filepath, 'a') as f:
            self.inc(print_num=print_num)
            line = self.dump(doc)
            f.write(line+"\n")
            if batch_size and batch_size > 0 and self.count % batch_size == 0 \
            and self.logger:
                self.logger.info(f"Processed {batch_size} items ({self.count} in total).")


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
    _interface = DBPersistenceInterface

    def __init__(self, item_name='record', **kwds):
        """Initialization method.

        Parameters
        ----------
        item_name : str
            Item name.
        **kwds :
            Keyword arguments used to construct `DBPersistenceInterface`
            if `settings=None`.
        """
        super().__init__(item_name, **kwds)

    def get_model_name(self):
        """Get model name."""
        return str(self.model)

    def drop_model_data(self, query=None, **kwds):
        """Drop model data.

        Parameters
        ----------
        query : callable
            If `None` then attribute `clear_model` is used.
            If callable then it is called on self (and `**kwds`)
            and the results is returned.
        **kwds :
            Optional keyword arguments passed to either 'query' or
            'self.clear_model' callable.

        Raises
        ------
        ValueError
            If query is not callable.
        """
        if query is None:
            if callable(self.clear_model):
                res = self.clear_model(self, **kwds)
            raise ValueError("'query' is not defined")
        if callable(query):
            res = query(self, **kwds)
        else:
            raise ValueError("'query' is not callable")
        mname = self.get_model_name()
        m = f"Model '{mname}' cleared with result {res}"
        self.logger.info(m)
        return res

    def prepare(self):
        """Prepare model before update."""
        if self.clear_model is not None:
            self.drop_model_data()
