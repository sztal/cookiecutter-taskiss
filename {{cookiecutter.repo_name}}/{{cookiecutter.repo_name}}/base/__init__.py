"""Module with general purpose base classes."""
from cerberus import Validator
from {{ cookiecutter.repo_name }}.base.abc import AbstractInterface


class BaseInterface(AbstractInterface):
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
        Default value is `_allow_default=True`.

    Notes
    -----
    *Cerberus* module provides very powerful means of data validation.
    Schema interface must be always implement with
    :py:class:`cerberus.Validator` objects.

    See Also
    --------
    cerberus
    """
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
        nm = self.__class__.__name__
        if self._schema is None:
            raise AttributeError(f"'{nm}' must implement 'schema' interface")
        if not isinstance(self._schema, Validator):
            msg = f"'{nm}' must implement 'schema' interface as 'cerberus.Validator' object"
            raise TypeError(msg)
        return self._schema
