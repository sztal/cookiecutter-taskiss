"""Mongoengine model classes."""
from mongoengine import Document
from mongoengine import ObjectIdField, StringField, IntField
from mongoengine.base import TopLevelDocumentMetaclass
from .mixins import BaseDocumentMixin
from {{ cookiecutter.repo_name }}.base.abc import AbstractMongoModelMetaclass



class ExampleMongoModel(Document, BaseDocumentMixin):
    """Example MongoDB model."""
    _id = ObjectIdField(primary_key=True)
    text = StringField(required=True)
    number = IntField(min=0, default=0)
    # Collection settings
    meta = { 'collection': 'example_collection' }
