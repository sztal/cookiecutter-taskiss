"""Base interfaces classes for handling complex method APIs.

Interface objects are meant to encapsulate complex APIs and arguments
validation if needed so the actual object that uses them does not
have to care about this.

Using :py:class:`{{ cookiecutter.repo_name }}.base.meta.Composable`
interfaces may be injected into a target object allowing for direct
argument / attribute access via standard attribute getter.
"""
from cerberus import Validator
from {{ cookiecutter.repo_name }}.utils.log import get_logger
from {{ cookiecutter.repo_name }}.utils.fetch import get_db_model
from .abc import AbstractInterfaceMetaclass
from .validators import BaseValidator


class BaseInterfaceMetaclass(AbstractInterfaceMetaclass):
    """Base interface metaclass providing 'schema' class property."""

    @property
    def schema(cls):
        """Schema getter."""
        schema = getattr(cls, '_schema', None)
        clsnm = cls.__name__
        if not schema:
            raise AttributeError(f"'{clsnm}' must implement 'schema' interface")
        if not isinstance(schema, Validator):
            msg = f"'{clsnm}' must implement 'schema' interface as 'cerberus.Validator' object"
            raise TypeError(msg)
        return schema

class BaseInterface(metaclass=BaseInterfaceMetaclass):
    """Base settings class.

    Attributes
    ----------
    schema : :py:class:`cerberus.Validator`
        Settings schema validator object.
        This should be usually defined as class level attribute.
        It is defined as property, so if `schema` property is not defined,
        then `_schema` attribute must be defined, as the getter is fetching it.
    _allow_default : bool
        Should default values be allowed.
    _defaultvalue : any
        Default value if `_allow_default=True`.

    Notes
    -----
    *Cerberus* module provides very powerful means of data validation.
    Schema interface must be always implement with
    :py:class:`cerberus.Validator` objects.

    See Also
    --------
    cerberus
    """
    _schema = None
    _allow_default = False
    _defaultvalue = None

    def __init__(self, **kwds):
        """Initialization method.

        Parameters
        ----------
        **kwds
            Settings.
        """
        arguments = self.schema.validated(kwds)
        if arguments is not None:
            for k, v in arguments.items():
                setattr(self, k, v)
        else:
            raise ValueError(f"Incorrect arguments {self.schema.errors}")

    def __getattr__(self, attr):
        """Default attribute value lookup."""
        if self._allow_default:
            return self._defaultvalue
        raise AttributeError

    @property
    def schema(self):
        """Schema getter."""
        return self.__class__.schema

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
        'logger': {
            'type': 'logger',
            'nullable': True,
            'default': None,
            'coerce': get_logger
        }
    })


class DBPersistenceInterface(BaseInterface):
    """Interface class for
    :py:class:`{{ cookiecutter.repo_name }}.persistence.DBPersistence`.

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
        'model': {
            'coerce': lambda x: get_db_model(x) if isinstance(x, str) else x,
            'nullable': False
        },
        'query': {},
        'processor': { 'type': 'callable', 'nullable': True, 'default': None },
        'batch_size': { 'type': 'integer', 'coerce': int, 'default': 0 },
        'n_retry': { 'type': 'integer', 'coerce': int, 'default': 2 },
        'backoff_time': { 'type': 'integer', 'coerce': int, 'default': 5 },
        'backoff_base': { 'type': 'number', 'default': 2, 'min': 0 },
        'logger': {
            'type': 'logger',
            'nullable': True,
            'default': None,
            'coerce': get_logger
        },
        'clear_model': { 'nullable': True, 'default': None }
    })
