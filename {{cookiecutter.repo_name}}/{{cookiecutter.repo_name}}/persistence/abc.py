"""Abstract base classes for persistence classes.

Persistence classes consist of database connectors/helpers
ODM/ORM models and helper classes for serialization and data
persistence on disk, in database and possibly by other means.
"""
from abc import ABCMeta, abstractmethod


class AbstractPersistenceConfig(metaclass=ABCMeta):
    """Abstract base persistence configuration class."""
    pass


class AbstractDBImporter(metaclass=ABCMeta):
    """Abstract base database importer class."""

    @property
    @abstractmethod
    def connection(self):
        """Database connection object."""
        pass

    @property
    @abstractmethod
    def cfg(self):
        """Importet configuration."""
        pass

    @property
    @abstractmethod
    def logger(self):
        """Logger object."""
        pass

    @property
    @abstractmethod
    def persistence(self):
        """Persistence object(s)."""
        pass
