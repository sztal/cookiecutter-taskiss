"""Base interfaces classes for handling complex method APIs.

Interface objects are meant to encapsulate complex APIs and arguments
validation if needed so the actual object that uses them does not
have to care about this.

Using :py:class:`{{ cookiecutter.repo_name }}.base.meta.Composable`
interfaces may be injected into a target object allowing for direct
argument / attribute access via standard attribute getter.
"""
from cerberus import Validator
from {{ cookiecutter.repo_name }}.base.abc import AbstractInterface
from {{ cookiecutter.repo_name }}.base.validators import BaseValidator
from {{ cookiecutter.repo_name }}.base import BaseInterface
from {{ cookiecutter.repo_name }}.utils.processors import parse_bool


class DiskPersistenceInterface(BaseInterface):
    """API interface object for
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
    _schema = BaseValidator({
        'filename': { 'type': 'string' },
        'dirpath': { 'type': 'string' },
        'batch_size': { 'type': 'integer', 'coerce': int, 'default': 0 },
        'logger': { 'type': 'logger', 'nullable': True, 'default': None }
    })


class DBPersistenceInterface(BaseInterface):
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
    _schema = BaseValidator({
        'model': { 'coerce': lambda x: get_db_model(x) if isinstance(x, str) else x },
        'query': {},
        'processor': { 'type': 'callable', 'nullable': True, 'default': None },
        'batch_size': { 'type': 'integer', 'coerce': int, 'default': 0 },
        'n_retry': { 'type': 'integer', 'coerce': int, 'default': 2 },
        'backoff_time': { 'type': 'integer', 'coerce': int, 'default': 5 },
        'backoff_base': { 'type': 'number', 'default': 2, 'min': 0 },
        'logger': { 'type': 'logger', 'nullable': True, 'default': None }
    })


class ScrapyCLIExtraArgsInterface(BaseInterface):
    """Interface for extra args provided in *Scrapy* CLI.

    :py:module:`{{ cookiecutter.repo_name }}.webscraping` module adds
    several additional command-line arguments that may be passed to
    *Scrapy* spiders to modify their behaviour. This interface is used
    to handle these arguments in an orderly fashion.

    Attributes
    ----------
     limit : int or None
        Limit for number of requests being made.
    mode : str or None
        Special mode the spider is run in.
        Currently only value `debug` is supported and it set a `pdb`
        breakpoint in the parse method right before the return statement.
    storage : str or None
        Type of storage used for data persistence.
        If `None` then both disk and database storage is used.
        Value `all` is an alias for `None`.
        If it is `nodb` the only disk persistence is used.
        If it is `no` then no persistence is used.
        Other values raise `ValueError`.
    overwrite : bool or None
        If `True` then data for given source is deleted before running the spider.
    test_url : str or None
        Single url to fetch and parse. Meant for testing purposes.
    """
    _schema = BaseValidator({
        'limit': {
            'type': 'integer',
            'coerce': int,
            'min': 1,
            'nullable': True,
            'default': None
        },
        'mode': {
            'type': 'string',
            'allowed': [ 'debug' ],
            'nullable': True,
        },
        'storage': {
            'type': 'string',
            'allowed': [ 'all', 'nodb', 'no' ],
            'nullable': True,
            'default': None
        },
        'overwrite': {
            'type': 'boolean',
            'coerce': parse_bool,
            'nullable': True,
            'default': None
        },
        'text_url': {
            'type': 'string',
            'nullable': True,
            'default': None
        }
    })
