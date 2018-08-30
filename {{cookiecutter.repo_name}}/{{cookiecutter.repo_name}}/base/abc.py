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

class AbstractDBMixinMetaclass(ABCMeta):
    """Abstract database mixin metaclass."""
    pass

class AbstractMongoModelMetaclass(AbstractDBModelMetaclass):
    """Abstract *MongoDB* model metaclass."""
    pass

class AbstractImporterMetaclass(ABCMeta):
    """Abstract database importer metaclass."""
    @property
    @abstractmethod
    def schema(cls):
        """Schema getter."""
        pass

class AbstractPersistenceMetaclass(ABCMeta):
    """Abstract persistence metaclass."""
    @property
    @abstractmethod
    def schema(cls):
        """Schema getter."""
        pass

# Abstract classes ------------------------------------------------------------

class AbstractDBConnector(metaclass=AbstractDBConnectorMetaclass):
    """Abstract base class for registering database connection objects."""
    pass


class AbstractDBModel(metaclass=AbstractDBModelMetaclass):
    """Abstract base class for registering database model classes."""
    pass

class AbstractDBMixin(metaclass=AbstractDBMixinMetaclass):
    """Abstract base class for registering database mixin classes."""
    pass

class AbstractMongoModel(AbstractDBModel):
    """Abstract base class for registering MongoDB model classes."""
    pass

class AbstractPersistence(metaclass=AbstractPersistenceMetaclass):
    """Abstract base class for registering persistence classes."""
    pass
