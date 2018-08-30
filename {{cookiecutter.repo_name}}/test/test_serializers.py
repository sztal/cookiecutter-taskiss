"""Test cases for :py:module:`{{ cookiecutter.repo_name }}.utils.serializers`."""
import json
from datetime import datetime
from {{ cookiecutter.repo_name }}.utils.serializers import JSONEncoder


class TestJSONEncoder:
    """Test cases for
    :py:class:`{{ cookiecutter.repo_name }}.utils.serializers.JSONEncoder`.
    """
    def test_dump(self):
        now = datetime.now()
        jsonified = json.loads(json.dumps(now, cls=JSONEncoder))
        assert jsonified == now.isoformat()
