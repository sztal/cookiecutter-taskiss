"""Persistence configuration classes."""
from {{ cookiecutter.repo_name }}.persistence.abc import AbstractPersistenceConfig


class PersistenceConfig(AbstractPersistenceConfig):
    """Base persistence configuration class.

    Attributes
    ----------
    batch_size : int or None
        Batch size when updating.
        If negative or *falsy* then no batch limit is used.
    logger : :py:class:`logging.Logger`
        Optional logger object.
    """
    def __init__(self, batch_size=None, logger=None):
        """Initialization method."""


class DiskPersistenceConfig(PersistenceConfig):
    """Configuration object for
    :py:class:`{{ cookiecutter.repo_name }}.persistence.DiskPersistence` objects.

    Attributes
    ----------
    filename : str
        Filename format string.
        Should have '{n}' in place of persistence file number.
    dirpath : str
        Absolute path to the persistence directory.
    batch_size : int or None
        Batch size when updating. It is used only to set logging intervals.
        If negative or *falsy* then no batch limit is used.
    logger : :py:class:`logging.Logger`
        Optional logger object.
    """
    def __init__(self, filename, dirpath):
        """Initialization method."""
        self.filename = filename
        self.dirpath = dirpath


class DBPersistenceConfig(PersistenceConfig):
    """Configuration object for
    :py:class:`{{ cookiecutter.repo_name }}.persistence.DBPersistence` objects.

    Attributes
    ----------
    model : a database connection or model
        Any kind of connector / connection / model object.
    query : callable or any
        Some object representing the update query.
        If callable then it is evaluated on the array of records to update.
    processor : callable or None
        Optional callable to evaluate over all individual records (like map).
    batch_size : int or None
        Batch size when updating.
        If negative or *falsy* then no batch limit is used.
    n_retry : int or None
        Number of retries after fail.
        If negative of *falsy* then only one update attempt is made.
    backoff_time : int or None
        Number of seconds to wait before trying to update again after a failure.
        If negative or *falsy*, then no backoff time is used.
    backoff_base : numeric
        Base for exponential backoff scaling of wait times between
        subsequent update attempts. Set to 1 to use constant backoff time.
        Must be non-negative.
    logger : :py:class:`logging.Logger`
        Optional logger object.
    """
    def __init__(self, model, query, processor=None, batch_size=None, n_retry=2,
                 backoff_time=5, backoff_base=2, logger=None):
        """Initialization method."""
        if backoff_base < 0:
            raise ValueError("'backoff_base' must be non-negative")
        self.model = model
        self.query = query
        self.processor = processor
        self.batch_size = batch_size
        self.n_retry = n_retry
        self.backoff_time = backoff_time
        self.backoff_base = backoff_base
        self.logger = logger
