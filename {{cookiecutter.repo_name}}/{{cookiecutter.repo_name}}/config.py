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
from configparser import ConfigParser, ExtendedInterpolation, _UNSET

MODE = os.environ.get('RUNTIME_MODE', 'DEV')
TOP_PATH = os.path.dirname(__file__)
ROOT_PATH = os.path.split(TOP_PATH)[0]


class Config(ConfigParser):
    """Config parser supporting reading from envvars."""

    def getenvvar(self, section, option, *, convert_bool=False,
                  fallback=_UNSET, **kwds):
        """Get value from environmental variable."""
        value = self.get(section, option, fallback=fallback, **kwds)
        try:
            value = os.environ[value]
        except KeyError:
            if fallback is _UNSET:
                raise KeyError(f"Environment variable '{option}' is not defined")
            else:
                return fallback
        if convert_bool:
            value = self._convert_to_boolean(value)
        return value


def get_cfg_path(cfgname='core.cfg'):
    """Get path to a config object."""
    if not cfgname.endswith('.cfg'):
        cfgname += '.cfg'
    return os.path.join(ROOT_PATH, 'cfg', cfgname)


cfg = Config(interpolation=ExtendedInterpolation())
with open(get_cfg_path(), 'r') as f:
    cfg.read(get_cfg_path())
