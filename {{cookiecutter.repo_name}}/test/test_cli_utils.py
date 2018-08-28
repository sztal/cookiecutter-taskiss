"""Test cases for command-line interface related utilities."""
import pytest
from {{ cookiecutter.repo_name }}.cli.utils import parse_args
from {{ cookiecutter.repo_name}}.cli.exceptions import MalformedArgumentError, RepeatedArgumentError


@pytest.mark.parametrize('args,eval_args,repeated,exp', [
    (["x=10", "y=20"], False, False, {'x': '10', 'y': '20'}),
    (["x=10", "y={'a': 1, 'b': 2}"], True, False, {'x': 10, 'y': {'a': 1, 'b': 2}}),
    (["10"], False, False, MalformedArgumentError),
    (["x=10", "x=20"], False, False, RepeatedArgumentError),
    (["x=10", "x=20"], True, True, {'x': [10, 20]})
])
def test_parse_args(args, eval_args, repeated, exp):
    """Test cases for `parse_args`."""
    if isinstance(exp, type) and issubclass(exp, Exception):
        with pytest.raises(exp):
            parse_args(*args, eval_args=eval_args, repeated=repeated)
    else:
        assert parse_args(*args, eval_args=eval_args, repeated=repeated) == exp
