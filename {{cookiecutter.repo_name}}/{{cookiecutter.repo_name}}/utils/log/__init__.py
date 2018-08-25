"""_{{ cookiecutter.repo_name | capitalize }}_ logging submodule."""

# pylint: disable=C0301

import os
import logging.config
from {{ cookiecutter.repo_name }}.utils.path import make_path


def init(root_path):
    """Initialize logging module."""
    settings = make_logging_settings(root_path)
    logging.config.dictConfig(settings)
    return settings

FORMATTERS = {
    'default': {
        'format': "[%(asctime)s] %(name)s | %(levelname)s | %(module)s | %(funcName)s | %(message)s",
        'datefmt': "%Y-%m-%d %H:%M:%S"
    },
    'message': {
        'format': "[%(asctime)s] %(message)s",
        'datefmt': "%Y-%m-%d %H:%M:%S"
    }
}

def make_logging_settings(root_path):
    """Make logging settings dict.

    Parameters
    ----------
    root_path : str
        Path to the root folder.
    """
    settings = {
        'version': 1,
        'disable_existing_loggers': True,
        'formatters': FORMATTERS,
        'handlers': {
            'default': {
                'class': 'logging.handlers.RotatingFileHandler',
                'level': 'INFO',
                'formatter': 'default',
                'filename': make_path(root_path, '{{ cookiecutter.repo_name }}', '{{ cookiecutter.repo_name }}.log'),
                'maxBytes': 1048576,
                'backupCount': 3
            },
            'error': {
                'class': 'logging.handlers.RotatingFileHandler',
                'level': 'WARNING',
                'formatter': 'default',
                'filename': make_path(root_path, '{{ cookiecutter.repo_name }}', 'error.log'),
                'maxBytes': 1048576,
                'backupCount': 3
            },
            'message': {
                'class': 'logging.StreamHandler',
                'level': 'INFO',
                'formatter': 'message',
                'stream': 'ext://sys.stdout'
            },
            'debug': {
                'class': 'logging.StreamHandler',
                'level': 'DEBUG',
                'formatter': 'default',
                'stream': 'ext://sys.stdout'
            },
            'taskiss': {
                'class': 'logging.handlers.RotatingFileHandler',
                'level': 'INFO',
                'formatter': 'default',
                'filename': make_path(root_path, 'taskiss', 'taskiss.log'),
                'maxBytes': 1048576,
                'backupCount': 3
            },
            'taskiss_error': {
                'class': 'logging.handlers.RotatingFileHandler',
                'level': 'WARNING',
                'formatter': 'default',
                'filename': make_path(root_path, 'taskiss', 'error.log'),
                'maxBytes': 1048576,
                'backupCount': 3
            }
        },
        'root': {
            'handlers': [
                'default',
                'error'
            ],
            'level': 'INFO'
        },
        'loggers': {
            'debug': {
                'propagate': False,
                'handlers': [ 'debug' ],
                'level': 'DEBUG'
            },
            'message': {
                'propagate': False,
                'handlers': [
                    'default',
                    'message'
                ],
                'level': 'INFO'
            },
            'taskiss': {
                'propagate': False,
                'hanlders': [
                    'taskiss',
                    'taskiss_error'
                ],
                'level': 'INFO'
            }
        }
    }
    return settings

def make_scrapy_logging_settings(root_path):
    """Make logging settings dict.

    Parameters
    ----------
    root_path : str
        Path to the root folder.
    """
    settings = {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': FORMATTERS,
        'handlers': {
            'scrapy': {
                'class': 'logging.handlers.RotatingFileHandler',
                'level': 'INFO',
                'formatter': 'default',
                'filename': make_path(root_path, 'scrapy', 'scrapy.log'),
                'maxBytes': 1048576,
                'backupCount': 3
            },
            'scrapy_error': {
                'class': 'logging.handlers.RotatingFileHandler',
                'level': 'WARNING',
                'formatter': 'default',
                'filename': make_path(root_path, 'scrapy', 'error.log'),
                'maxBytes': 1048576,
                'backupCount': 3
            },
            'scrapy_debug': {
                'class': 'logging.handlers.RotatingFileHandler',
                'level': 'DEBUG',
                'formatter': 'default',
                'filename': make_path(root_path, 'scrapy', 'debug.log'),
                'maxBytes': 1048576,
                'backupCount': 2
            }
        },
        'root': {
            'propagate': False,
            'handlers': [
                'scrapy',
                'scrapy_error'
            ],
            'level': 'INFO'
        }
    }
    return settings
