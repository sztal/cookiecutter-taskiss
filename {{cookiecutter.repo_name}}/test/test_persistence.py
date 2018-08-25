"""Test cases for :py:mod:`{{ cookiecutter.repo_name }}.persistence`."""
import os
import json
import pytest
from datetime import datetime
from {{ cookiecutter.repo_name }}.persistence import JSONLinesPersistence


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


class TestJSONLinesPersistence:
    """Test cases for
    :py:mod:`{{ cookiecutter.repo_name }}.persistence.JSONLinesPersistence`.
    """

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
