"""Webscraping related interface classes."""
from {{ cookiecutter.repo_name }}.utils.processors import parse_bool
from {{ cookiecutter.repo_name }}.base.validators import BaseValidator
from {{ cookiecutter.repo_name }}.base.interface import BaseInterface


class ScrapyCLIExtraArgsInterface(BaseInterface):
    """Interface for extra args provided in *Scrapy* CLI.

    :py:module:`{{ cookiecutter.repo_name }}.webscraping` module adds
    several additional command-line arguments that may be passed to
    *Scrapy* spiders to modify their behaviour. This interface is used
    to handle these arguments in an orderly fashion.

    Attributes
    ----------
     limit : int or None
        Limit for number of requests being made.
    mode : str or None
        Special mode the spider is run in.
        Currently only value `debug` is supported and it set a `pdb`
        breakpoint in the parse method right before the return statement.
    storage : str or None
        Type of storage used for data persistence.
        If `None` then both disk and database storage is used.
        Value `all` is an alias for `None`.
        If it is `nodb` the only disk persistence is used.
        If it is `no` then no persistence is used.
        Other values raise `ValueError`.
    overwrite : bool or None
        If `True` then data for given source is deleted before running the spider.
    test_url : str or None
        Single url to fetch and parse. Meant for testing purposes.
    """
    _schema = BaseValidator({
        'limit': {
            'type': 'integer',
            'coerce': int,
            'min': 1,
            'nullable': True,
            'default': None
        },
        'mode': {
            'type': 'string',
            'allowed': [ 'debug', None ],
            'nullable': True,
            'coerce': lambda x: str(x).lower() if x else x
        },
        'storage': {
            'type': 'string',
            'allowed': [ 'all', 'nodb', 'no', None ],
            'nullable': True,
            'default': None,
            'coerce': lambda x: str(x).lower() if x else x
        },
        'overwrite': {
            'type': 'boolean',
            'coerce': parse_bool,
            'nullable': True,
            'default': None
        },
        'text_url': {
            'type': 'string',
            'nullable': True,
            'default': None
        }
    })
