"""Abstract base classes for persistence classes.

Persistence classes consist of database connectors/helpers
ODM/ORM models and helper classes for serialization and data
persistence on disk, in database and possibly by other means.
"""
from abc import ABCMeta, abstractmethod


class AbstractPersistence(metaclass=ABCMeta):
    """Abstract base persistence class."""

    @property
    @abstractmethod
    def count(self):
        """Count of processed items."""
        pass

    @property
    @abstractmethod
    def cfg(self):
        """Persistence config."""
        pass

    @abstractmethod
    def persist(self):
        """Persist a data point / object."""
        pass

    @abstractmethod
    def inc(self):
        """Increment counter."""
        pass
