"""Test cases for command-line interface related utilities."""
import pytest
from {{ cookiecutter.repo_name }}.cli.utils import parse_args
from {{ cookiecutter.repo_name}}.cli.exceptions import MalformedArgumentError, RepeatedArgumentError


@pytest.mark.parametrize('args,parser,repeated,exp', [
    (['x=10', 'y=20'], None, False, {'x': '10', 'y': '20'}),
    (['x=10', 'y={"a": 1, "b": 2}'], 'json', False, {'x': 10, 'y': {'a': 1, 'b': 2}}),
    (['x=10', 'y={"a": 1, "b": 2}'], 'eval', False, {'x': 10, 'y': {'a': 1, 'b': 2}}),
    (['10'], None, False, MalformedArgumentError),
    (['x=10', 'x=20'], None, False, RepeatedArgumentError),
    (['x=10', 'x=20'], 'json', True, {'x': [10, 20]}),
    (['x=10', 'x=20'], 'eval', True, {'x': [10, 20]})
])
def test_parse_args(args, parser, repeated, exp):
    """Test cases for `parse_args`."""
    if isinstance(exp, type) and issubclass(exp, Exception):
        with pytest.raises(exp):
            parse_args(*args, parser=parser, repeated=repeated)
    else:
        assert parse_args(*args, parser=parser, repeated=repeated) == exp
