"""Importer classes.

Importers are helper objects responsible for importing data to various storage
facilities. They are meant to be composed of
:py:module:`{{ cookiecutter.repo_name }}.persistence` objects.
"""
# pylint: disable=E1101,W0221
import json


class DataImporter:
    """Data importer base class."""

    def __init__(self, persistence):
        """Initialization method.

        Parameters
        ----------
        persistence : persistence object
            Object inheriting from
            :py:class:{{ cookiecutter.repo_name }}
        """
        self.persistence = persistence

    def import_data(self, data, print_num=True, **kwds):
        """Import data function.

        Parameters
        ----------
        data : iterable
            Sequence of data records to import.
        print_num : bool
            Should number of processed documents be printed.
        **kwds :
            Other arguments passed to `persist` method.
        """
        with self.persistence:
            for record in data:
                self.persistence.persist(record, print_num=print_num, **kwds)


class JSONLinesImporter(DataImporter):
    """JSON lines data importer."""

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

    def import_data(self, src, print_num=True, **kwds):
        """Import data method.

        Parameters
        ----------
        src : str
            Path to the data source.
        **kwds :
            Other arguments passed to `persist` method.
        """
        data = self.read_data(src)
        super().import_data(data, print_num=print_num, **kwds)
