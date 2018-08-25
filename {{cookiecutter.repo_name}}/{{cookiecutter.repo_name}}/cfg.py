"""Configuration module that defines basic information needed by all modules.

Attributes
----------
MODE : {'DEV', 'PROD'}
    Runtime mode.
TOP_PATH : str
    Absolute path to the package's top module.
ROOT_PATH : str
    Absolute path to the package root directory.
cfg : :py:class:`configparser.ConfigParser`
    Main config object.
"""
import os
from configparser import ConfigParser, ExtendedInterpolation


MODE = os.environ.get('RUNTIME_MODE', 'DEV')
TOP_PATH = os.path.dirname(__file__)
ROOT_PATH = os.path.split(TOP_PATH)[0]


def get_cfg_path(cfgname='core.cfg'):
    """Get path to a config object."""
    if not cfgname.endswith('.cfg'):
        cfgname += '.cfg'
    return os.path.join(ROOT_PATH, 'cfg', cfgname)

cfg = ConfigParser(interpolation=ExtendedInterpolation())
with open(get_cfg_path(), 'r') as f:
    cfg.read(get_cfg_path())
