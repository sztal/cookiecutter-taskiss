"""_{{ cookiecutter.repo_name | capitalize }}_ top-level module.

This module defines additional top-level exports, main package metadata etc.
"""
# pylint: disable=C0103
import os
from configparser import ConfigParser, ExtendedInterpolation
from {{ cookiecutter.repo_name }}.config import cfg, MODE
from {{ cookiecutter.repo_name }}.utils import log
from {{ cookiecutter.repo_name }}.utils.path import make_path
from {{ cookiecutter.repo_name }}.utils.processors import parse_bool
from {{ cookiecutter.repo_name }}.persistence import mongo


__author__ = '{{ cookiecutter.full_name }}'
__email__ = '{{ cookiecutter.email }}'
__version__ = '{{ cookiecutter.version }}'


# Iniitilize application components -------------------------------------------

log.init(cfg.getenvvar(MODE, 'log_root_dir'))
mdb = None
if cfg.getenvvar('DEV', 'db_use', fallback=True, convert_bool=True):
    mdb = mongo.init(
        user=cfg.getenvvar(MODE, 'mongo_user'),
        password=cfg.getenvvar(MODE, 'mongo_pass'),
        host=cfg.getenvvar(MODE, 'mongo_host'),
        port=cfg.getenvvar(MODE, 'mongo_port'),
        db=cfg.getenvvar(MODE, 'mongo_db')
    )
