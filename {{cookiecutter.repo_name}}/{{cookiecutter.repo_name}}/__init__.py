"""_{{ cookiecutter.repo_name | capitalize }}_ top-level module.

This module defines additional top-level exports, main package metadata etc.
"""
import os
from configparser import ConfigParser, ExtendedInterpolation
from {{ cookiecutter.repo_name }}.utils import log
from {{ cookiecutter.repo_name }}.utils.path import make_path

__author__ = '{{ cookiecutter.full_name }}'
__email__ = '{{ cookiecutter.email }}'
__version__ = '{{ cookiecutter.version }}'


MODE = os.environ.get('RUNTIME_MODE', 'DEV')
TOP_PATH = os.path.dirname(__file__)
ROOT_PATH = os.path.split(TOP_PATH)[0]

# Config object initilization -------------------------------------------------

def get_cfg_path(cfgname='core.cfg'):
    """Get path to a config object."""
    if not cfgname.endswith('.cfg'):
        cfgname += '.cfg'
    return os.path.join(ROOT_PATH, 'cfg', cfgname)

cfg = ConfigParser(interpolation=ExtendedInterpolation())
with open(get_cfg_path(), 'r') as f:
    cfg.read(get_cfg_path())

# Iniitilize application components -------------------------------------------

log.init(os.environ[cfg.get(MODE, 'log_root_dir')])

# Base path helpers -----------------------------------------------------------

def get_data_path(section, *args, **kwds):
    """Get path for the project data directory.

    Parameters
    ----------
    section : str
        Name of data section as defined in the config.
    *args :
        Path components.
    **kwds :
        Other arguments passed to `os.makedirs`.
    """
    dirpath = cfg.get(MODE, section)
    path = os.path.join(ROOT_PATH, dirpath, *args)
    return make_path(path, **kwds)

def get_rawdata_path(*args, **kwds):
    """Get rawdata project directory path.

    Parameters
    ----------
    *args :
        Path components.
    **kwds :
        Arguments passed to `get_data_path`.
    """
    return get_data_path('path_rawdata', *args, **kwds)

def get_persistence_path(*args, **kwds):
    """Get data persistence project directory path.

    Parameters
    ----------
    *args :
        Path components.
    **kwds :
        Arguments passed to `get_data_path`.
    """
    return get_data_path('path_persistence', *args, **kwds)
