"""_{{ cookiecutter.repo_name | capitalize }}_ top-level module.

This module defines additional top-level exports, main package metadata etc.
"""
# pylint: disable=C0103
import os
import atexit
from logging import getLogger
from configparser import ConfigParser, ExtendedInterpolation
from pymongo import MongoClient
from mongoengine.base import DocumentMetaclass
from {{ cookiecutter.repo_name }}.config import cfg, MODE
from {{ cookiecutter.repo_name }}.utils import log
from {{ cookiecutter.repo_name }}.utils.path import make_path
from {{ cookiecutter.repo_name }}.utils.processors import parse_bool
from {{ cookiecutter.repo_name }}.persistence.db import mongo as mongodb
from {{ cookiecutter.repo_name }}.persistence.importers import BaseImporter
from {{ cookiecutter.repo_name }}.persistence import BasePersistence
from {{ cookiecutter.repo_name }}.base.abc import AbstractDBConnector, AbstractMongoModel
from {{ cookiecutter.repo_name }}.taskiss import Taskiss


__author__ = '{{ cookiecutter.full_name }}'
__email__ = '{{ cookiecutter.email }}'
__version__ = '{{ cookiecutter.version }}'

# Register abstract base classes ----------------------------------------------

AbstractDBConnector.register(MongoClient)
AbstractMongoModel.register(DocumentMetaclass)

# Iniitilize application components -------------------------------------------

log.init(cfg.getenvvar(MODE, 'log_root_dir'))
logger = getLogger()

mongo = None
if cfg.getenvvar(MODE, 'use_mongo', fallback=True, convert_bool=True):
    mongo = mongodb.init(
        user=cfg.getenvvar(MODE, 'mongo_user'),
        password=cfg.getenvvar(MODE, 'mongo_pass'),
        host=cfg.getenvvar(MODE, 'mongo_host'),
        port=cfg.getenvvar(MODE, 'mongo_port'),
        db=cfg.getenvvar(MODE, 'mongo_db')
    )

taskiss = None
if cfg.getenvvar(MODE, 'use_celery', fallback=True, convert_bool=True):
    taskiss = Taskiss('{{cookiecutter.repo_name}}',
                      config_source='{{cookiecutter.repo_name}}.config.taskiss')
    taskiss.setup_scheduler()

# Exit hanlders ---------------------------------------------------------------

def exit_handler():
    """Exit handler that handles db logout etc."""
    db = cfg.getenvvar(MODE, 'mongo_db')
    user = cfg.getenvvar(MODE, 'mongo_user')
    mongo[db].logout()
    logger.info("Log out user '%s' from database '%s'", user, db)
    mongo.close()
    logger.info("MongoDB connection closed [%s]", mongo.name)

# atexit.register(exit_handler)

# -----------------------------------------------------------------------------
