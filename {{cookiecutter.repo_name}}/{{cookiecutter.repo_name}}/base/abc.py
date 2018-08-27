"""Abstract base classes."""
from abc import ABCMeta, abstractmethod


class AbstractInterface(metaclass=ABCMeta):
    """Abstract base class for settings objects."""
    _schema = None

    @property
    @abstractmethod
    def schema(self):
        """Schema getter."""
        pass


class AbstractDBConnector(metaclass=ABCMeta):
    """Abstract base class for registering database connection objects."""
    pass
