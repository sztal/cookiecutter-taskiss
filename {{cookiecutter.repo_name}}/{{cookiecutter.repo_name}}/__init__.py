"""_{{ cookiecutter.repo_name | capitalize }}_ top-level module.

This module defines additional top-level exports, main package metadata etc.
"""
# pylint: disable=C0103
import os
import atexit
from logging import getLogger
from configparser import ConfigParser, ExtendedInterpolation
from pymongo import MongoClient
from mongoengine.base import BaseDocument, DocumentMetaclass, TopLevelDocumentMetaclass
from {{ cookiecutter.repo_name }}.config import cfg, MODE
from {{ cookiecutter.repo_name }}.utils import log
from {{ cookiecutter.repo_name }}.utils.path import make_path
from {{ cookiecutter.repo_name }}.utils.processors import parse_bool
from {{ cookiecutter.repo_name }}.persistence.db import mongo
from {{ cookiecutter.repo_name }}.persistence.importers import BaseDBImporter
from {{ cookiecutter.repo_name }}.persistence import BasePersistence
from {{ cookiecutter.repo_name }}.base.abc import AbstractDBConnector, AbstractMongoModel
from {{ cookiecutter.repo_name }}.base.abc import AbstractDBImporter, AbstractPersistence


__author__ = '{{ cookiecutter.full_name }}'
__email__ = '{{ cookiecutter.email }}'
__version__ = '{{ cookiecutter.version }}'

# Register abstract base classes ----------------------------------------------

AbstractDBConnector.register(MongoClient)
AbstractMongoModel.register(BaseDocument)
AbstractMongoModel.register(DocumentMetaclass)
AbstractMongoModel.register(TopLevelDocumentMetaclass)
AbstractDBImporter.register(BaseDBImporter)
AbstractPersistence.register(BasePersistence)

# Iniitilize application components -------------------------------------------

log.init(cfg.getenvvar(MODE, 'log_root_dir'))
logger = getLogger()
mdb = None
if cfg.getenvvar('DEV', 'db_use', fallback=True, convert_bool=True):
    mdb = mongo.init(
        user=cfg.getenvvar(MODE, 'mongo_user'),
        password=cfg.getenvvar(MODE, 'mongo_pass'),
        host=cfg.getenvvar(MODE, 'mongo_host'),
        port=cfg.getenvvar(MODE, 'mongo_port'),
        db=cfg.getenvvar(MODE, 'mongo_db')
    )

# Exit hanlders ---------------------------------------------------------------

def exit_handler():
    """Exit handler that handles db logout etc."""
    db = cfg.getenvvar(MODE, 'mongo_db')
    user = cfg.getenvvar(MODE, 'mongo_user')
    mdb[db].logout()
    logger.info("Log out user '%s' from database '%s'", user, db)
    mdb.close()
    logger.info("MongoDB connection closed [%s]", mdb.name)

atexit.register(exit_handler)

# -----------------------------------------------------------------------------
