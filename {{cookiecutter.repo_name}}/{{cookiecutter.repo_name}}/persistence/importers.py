"""Importer classes.

Importers are helper objects responsible for importing data to various storage
facilities. They are meant to be composed of
:py:module:`{{ cookiecutter.repo_name }}.persistence` objects.
"""
# pylint: disable-all
from collections import Mapping
import json
from {{ cookiecutter.repo_name }}.base.validators import copy_schema
from {{ cookiecutter.repo_name }}.base.abc import AbstractImporterMetaclass
from {{ cookiecutter.repo_name }}.base.validators import ImporterValidator


class BaseImporterMetaclass(AbstractImporterMetaclass):
    """Base importer metaclass providing 'schema' class property."""

    @property
    def schema(cls):
        """Schema getter."""
        cn = cls.__name__
        if not getattr(cls, '_schema', None):
            raise Attribute(f"'{cn}' does not define 'schema' attribute")
        if isinstance(cls._schema, dict):
            cls._schema = ImporterValidator(cls._schema)
        return cls._schema


class BaseImporter(metaclass=BaseImporterMetaclass):
    """Data importer base class."""
    _schema =  {
        'source': { 'type': 'sequence', 'nullable': False },
        'print_num': {
            'type': 'boolean',
            'default': True
        },
        'persistence': { 'type': 'string' }
    }

    def __init__(self, persistence):
        """Initialization method.

        Parameters
        ----------
        persistence : persistence object
            Object inheriting from
            :py:class:{{ cookiecutter.repo_name }}
        """
        self.persistence = persistence

    @property
    def schema(self):
        """Schema getter."""
        return self.__class__.schema

    def import_data(self, source, print_num=True, **kwds):
        """Import data function.

        Parameters
        ----------
        source : sequence
            Sequence of data records to import.
        print_num : bool
            Should number of processed documents be printed.
        **kwds :
            Other arguments passed to `persist` method.
        """
        with self.persistence:
            for record in source:
                self.persistence.persist(record, print_num=print_num, **kwds)


class JSONLinesImporter(BaseImporter):
    """JSON lines data importer."""
    interface = {
        **BaseImporter.schema.schema,
        'source': { 'type': 'string', 'nullable': False }
    }

    def read_data(self, src):
        """Read JSON lines file and import to a storage facility.

        Parameters
        ----------
        src : str
            Path to the data source.
        print_num : bool
            Should number of processed documents be printed.
        **kwds :
            Other arguments passed to `persist` method.
        """
        if not src:
            raise ValueError(
                "{}: no data source path.".format(self.__class__.__name__)
            )
        with open(src, 'rb') as f:
            for line in f:
                try:
                    line = line.decode('utf-8')
                except UnicodeDecodeError:
                    if self.logger:
                        errmsg = "Malformed unicode content at record no. {} [{}].".format(
                            self.n_processed, str(line)
                        )
                        self.logger.error(errmsg)
                    line = line.decode('utf-8', 'ignore')
                data = json.loads(line.strip())
                yield data

    def import_data(self, source, print_num=True, **kwds):
        """Import data method.

        Parameters
        ----------
        source : str
            Path to the data source.
        **kwds :
            Other arguments passed to `persist` method.
        """
        data = self.read_data(source)
        super().import_data(data, print_num=print_num, **kwds)
