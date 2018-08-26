"""Abstract base classes."""
from abc import ABCMeta, abstractmethod
from cerberus import Validator


class AbstractInterface(metaclass=ABCMeta):
    """Abstract base class for settings objects."""
    _schema = None

    @property
    @abstractmethod
    def schema(self):
        """Schema getter."""
        pass
