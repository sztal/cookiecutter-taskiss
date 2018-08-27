"""Mongoengine model classes."""
from mongoengine import Document
from mongoengine import ObjectIdField, StringField, IntField
from {{ cookiecutter.repo_name }}.persistence.db.mongo.mixins import BaseDocumentMixin


class ExampleMongoModel(Document, BaseDocumentMixin):
    """Example MongoDB model."""
    _id = ObjectIdField(primary_key=True)
    text = StringField(required=True)
    number = IntField(min=0, default=0)
    # Collection settings
    meta = { 'collection': 'example_collection' }
