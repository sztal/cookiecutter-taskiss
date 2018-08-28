"""Utility functions for importers CLI module."""
from logging import getLogger
from {{ cookiecutter.repo_name }}.cli.utils import pprint, show_unique
from {{ cookiecutter.repo_name }}.utils.fetch import iter_importers
from {{ cookiecutter.repo_name }}.utils.fetch import get_persistence, get_importer


def show_importers():
    """Show registered database importers."""
    show_unique(iter_importers())

def show_importer_schema(path_or_name):
    """Show database importer schema.

    Parameters
    ----------
    path_or_name : str
        Proper python path or class name.
    """
    importer = get_importer(path_or_name)
    schema = importer.get_schema().schema
    pprint(schema)

def run_importer(importer, persistence, log=False, **kwds):
    """Run database data importer.

    Parameters
    ----------
    importer : str
        Importer class specified as a fully qualified python path
        or a class name.
    persistence : str
        Persistence class specified as a fully qualified python path
        or a class name.
    log : bool
        Should action be logged.
    **kwds :
        Keyword arguments passed both to the importer and the persistence.
        This can be done without any risk thanks to the interfaces.
    """
    persistence = get_persistence(persistence)(**kwds)
    importer = get_importer(importer)(persistence)
    importer_kwds = importer.schema.validated(kwds)
    if not kwds:
        raise ValueError(importer.schema.errors)
    if log:
        logger = getLogger('message')
        logger.info("Importing data with %r [%r] to %r [%r]",
                    importer, importer_kwds, persistence, kwds)
    importer.import_data(**importer_kwds)
