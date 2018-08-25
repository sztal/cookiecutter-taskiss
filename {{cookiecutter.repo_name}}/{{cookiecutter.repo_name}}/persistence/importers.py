"""Importer classes.

Importers are helper objects responsible for importing data to various storage
facilities. They are meant to be composed of
:py:mod:`{{ cookiecutter.repo_name }}.persistence` objects.
"""
# pylint: disable=E1101
import json
from {{ cookiecutter.repo_name }}.meta import Composable
from {{ cookiecutter.repo_name }}.persistence import MongoPersistence
from {{ cookiecutter.repo_name }}.persistence.abc import AbstractDBImporter


class DataImporter(metaclass=Composable):
    """Data importer base class.

    Attributes
    ----------
    model : mongoengine.Document
        Mongoengine collection model.
    key_field : str
        Name of the key field for updating.
    batch_size : int
        Passed to `MongoPersistence` object.
    action_hook : func
        Passed to `MongoPersistence` object,
    logger : bool or str
        Passed to `MongoPersistence` object.
    """
    __components = [
        ('persistence', MongoPersistence())
    ]

    def __init__(self, model, query_fields, batch_size=None,
                 action_hook=None, logger=None):
        """Initialization method."""
        self.persistence._set_attributes(
            model=model,
            query_fields=query_fields,
            batch_size=batch_size,
            action_hook=action_hook,
        )
        if logger is not None:
            self.persistence.set_logger(logger)


class JsonImporter(DataImporter):
    """JSON data importer.

    Attributes
    ----------
    model : mongoengine.Document
        Mongoengine collection model.
    key_field : str or iterable of str
        Name of the key field for updating.
    batch_size : int
        Batch size for inserting/updating data.
    src : str
        Optional path to the source file.
        It may be also specified as an argument to the `import_data` method.
    """

    def __init__(self, model, query_fields, batch_size=None,
                 action_hook=None, logger=None, src=None):
        """Initialization method."""
        super().__init__(model, query_fields, batch_size, action_hook, logger)
        self.src = src

    def import_data(self, src=None, print_num=True, **kwds):
        """Read file and transform to j.

        Parameters
        ----------
        src : str
            Path to the data source.
        update : bool
            Should update be done instead of insert.
        print_num : bool
            Should number of processed documents be printed.
        **kwds :
            Other arguments passed to `MongoPersistence.update`.
        """
        if not src:
            src = self.src
        if not src:
            raise ValueError(
                "{}: no data source path.".format(self.__class__.__name__)
            )
        with open(src, 'rb') as f:
            for line in f:
                try:
                    line = line.decode('utf-8')
                except UnicodeDecodeError:
                    errmsg = "Malformed unicode content at record no. {} [{}].".format(
                        self.n_processed, str(line)
                    )
                    self.logger.error(errmsg)
                    line = line.decode('utf-8', 'ignore')
                data = json.loads(line.strip())
                self.persist(data, print_num=print_num, **kwds)
        self.persist(min_batch_size=0)
