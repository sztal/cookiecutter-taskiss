"""Abstract base classes."""
from abc import ABCMeta, abstractmethod


# Abstract metaclasses --------------------------------------------------------

class AbstractInterfaceMetaclass(ABCMeta):
    """Abstract interface metaclass."""
    pass

class AbstractDBConnectorMetaclass(ABCMeta):
    """Abstract database connector metaclass."""
    pass

class AbstractDBModelMetaclass(ABCMeta):
    """Abstract database model metaclass."""
    pass

class AbstractDBImporterMetaclass(ABCMeta):
    """Abstract database importer metaclass."""
    pass

class AbstractPersistenceMetaclass(ABCMeta):
    """Abstract persistence metaclass."""
    pass


# Abstract classes ------------------------------------------------------------

class AbstractInterface(metaclass=AbstractInterfaceMetaclass):
    """Abstract base class for settings objects."""
    _schema = None

    @property
    @abstractmethod
    def schema(self):
        """Schema getter."""
        pass


class AbstractDBConnector(metaclass=AbstractDBConnectorMetaclass):
    """Abstract base class for registering database connection objects."""
    pass


class AbstractDBModel(metaclass=AbstractDBModelMetaclass):
    """Abstract base class for registering database model classes."""
    pass

class AbstractMongoModel(AbstractDBModel):
    """Abstract base class for registering MongoDB model classes."""
    pass

class AbstractDBImporter(metaclass=AbstractDBImporterMetaclass):
    """Abstract base class for registering db importers classes."""
    pass

class AbstractPersistence(metaclass=AbstractPersistenceMetaclass):
    """Abstract base class for registering persistence classes."""
    pass
