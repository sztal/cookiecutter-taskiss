"""Test cases for `utils.string`."""
import hashlib
import pytest
from {{ cookiecutter.repo_name }}.utils.string import hash_string


@pytest.mark.parametrize('string', ['user1', 'user2'])
@pytest.mark.parametrize('salt', [None, 'rfwze'])
def test_hash_string(string, salt):
    """Test cases for `hash_string`."""
    res = hash_string(string, salt)
    string = string + salt if salt else string
    exp = hashlib.md5(string.encode('utf-8')).hexdigest()
    assert res == exp
