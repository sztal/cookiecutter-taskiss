"""Abstract base classes for persistence classes.

Persistence classes consist of database connectors/helpers
ODM/ORM models and helper classes for serialization and data
persistence on disk, in database and possibly by other means.
"""
from abc import ABCMeta, abstractmethod


class AbstractPersistenceConfig(metaclass=ABCMeta):
    """Abstract base persistence configuration class."""
    pass


class AbstractImporter(metaclass=ABCMeta):
    """Abstract data importer base class."""

    @abstractmethod
    def import_data(self):
        """Import data method."""
        pass
