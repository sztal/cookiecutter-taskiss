"""_{{ cookiecutter.repo_name | capitalize }}_ top-level module.

This module defines additional top-level exports, main package metadata etc.
"""
import os
from configparser import ConfigParser, ExtendedInterpolation
from {{ cookiecutter.repo_name }}.cfg import cfg, MODE
from {{ cookiecutter.repo_name }}.utils import log
from {{ cookiecutter.repo_name }}.utils.path import make_path
from {{ cookiecutter.repo_name }}.utils.processors import parse_bool
from {{ cookiecutter.repo_name }}.persistence import mongo


__author__ = '{{ cookiecutter.full_name }}'
__email__ = '{{ cookiecutter.email }}'
__version__ = '{{ cookiecutter.version }}'


# Iniitilize application components -------------------------------------------

log.init(os.environ[cfg.get(MODE, 'log_root_dir')])
mdb = None
if parse_bool(os.environ.get('DB_USE', True)):
    mdb = mongo.init(
        user=cfg.get(MODE, 'mongo_user'),
        password=cfg.get(MODE, 'mongo_pass'),
        host=cfg.get(MODE, 'mongo_host'),
        port=cfg.get(MODE, 'mongo_port'),
        db=cfg.get(MODE, 'mongo_db'),
        use_envvars=True
    )
