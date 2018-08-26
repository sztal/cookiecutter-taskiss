"""Test cases for :py:module:`{{ cookiecutter.repo_name }}.persistence`."""
import os
import json
from logging import getLogger
import pytest
from datetime import datetime
from mongoengine import Document
from mongoengine import ObjectIdField, StringField, IntField, ListField, DateTimeField
from {{ cookiecutter.repo_name }}.persistence import JSONLinesPersistence
from {{ cookiecutter.repo_name }}.persistence.mongo import MongoPersistence
from {{ cookiecutter.repo_name }}.persistence.importers import DataImporter
from {{ cookiecutter.repo_name }}.persistence.mongo.mixins import BaseDocumentMixin


@pytest.fixture
def jl_persistence():
    """Fixture: JSONLinesPersistence."""
    jl_persistence = JSONLinesPersistence(
        filename='jlpersistence-test-{n}.jl',
        dirpath=os.path.join(os.path.dirname(__file__), 'data', 'persistence')
    )
    yield jl_persistence
    #Teardown part of the fixture
    os.remove(jl_persistence.filepath)

@pytest.fixture(scope='module')
def MongoModel():
    """Fixture: test *Mongoengine* model."""
    class MongoModel(Document, BaseDocumentMixin):
        """ODM model."""
        _id = ObjectIdField(primary_key=True)
        title = StringField()
        views = IntField()
        tags = ListField()
        meta = {
            'collection': 'test_mongo_model'
        }
    yield MongoModel
    # Teardown part of the fixture
    MongoModel.drop_collection()

@pytest.fixture(scope='module')
def mongo_model_data():
    """Fixture: data for testing with `MongoModel`."""
    data = []
    for i in range(1550):
        x = {
            'title': f"t{i}",
            'views': i,
            'tags': [ 'a', 'b' ]
        }
        data.append(x)
    return data

@pytest.fixture(scope='module')
def importer(MongoModel):
    """Fixture: JSONLinesImporter."""
    importer = DataImporter(MongoPersistence(
        model=MongoModel,
        query='title',
        batch_size=440,
        logger=getLogger(),
        backoff_time=0
    ))
    return importer


class TestJSONLinesPersistence:
    """Test cases for `JSONLinesPersistence`."""

    def test_persist(self, jl_persistence):
        data = [ {'x': i, 'timestamp': datetime.now() } for i in range(1, 26) ]
        for x in data:
            jl_persistence.persist(x, print_num=False)
            assert x['x'] == jl_persistence.count
            # Dump timestamp to isoformat for final comparison
            x['timestamp'] = x['timestamp'].isoformat()
        # Compare entire datasets
        saved_data = [ item for item in jl_persistence.load_persisted_data() ]
        assert saved_data == data


@pytest.mark.db
class TestDataImporterAndMongoPersistence:
    """Test cases for `DataImporter` and `MongoPersistence`."""

    def test_import_and_persist(self, importer, mongo_model_data):
        """Test case for data import and persistence."""
        importer.import_data(mongo_model_data, print_num=True)

    def test_validate_db_data(self, MongoModel, mongo_model_data):
        """Test case for MongoDB connection and data validity after persistence."""
        data = [ doc.to_dict() for doc in MongoModel.objects.order_by('views') ]
        assert data == mongo_model_data
