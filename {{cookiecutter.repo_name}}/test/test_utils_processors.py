"""Test cases for `utils.processors`."""
import re
from datetime import datetime, date
import pytest
from {{ cookiecutter.repo_name }}.utils.processors import date_from_string, parse_date, parse_bool


@pytest.mark.parametrize('dt,fmt,exp', [
    ('2018-08-01', "%Y-%m-%d", datetime(2018, 8, 1)),
    ('2017-01-01 | 01:01:01', "%Y-%m-%d %H:%M:%S", datetime(2017, 1, 1, 1, 1, 1)),
])
@pytest.mark.parametrize('preprocessor,kwds', [
    (lambda x, sub, rx: rx.sub(sub, x), {
        'rx': re.compile(r"\s*?\|\s*?", re.IGNORECASE),
        'sub': r" "
    })
])
def test_date_parsers(dt, fmt, preprocessor, kwds, exp):
    """Test cases for `date_from_string` function."""
    res1 = date_from_string(dt, fmt, preprocessor, **kwds)
    res2 = parse_date(dt, preprocessor, **kwds)
    assert res1 == res2 == exp

@pytest.mark.parametrize('x,kwds,exp', [
    (True, {}, True),
    (False, {}, False),
    ('true', {}, True),
    ('no', {}, False),
    ('enable', {'add_true': ['enable']}, True),
    ('disable', {'add_false': ['disable']}, False),
    ('no way!', {'false': ['no way!']}, False),
    ('oh yes!', {'true': ['oh yes!']}, True),
    ('true', {'true': ['oh yes!']}, ValueError),
    ('no way!', {}, ValueError)
])
def test_parse_bool(x, kwds, exp):
    """Test cases for `parse_bool` function."""
    if isinstance(exp, type) and issubclass(exp, Exception):
        with pytest.raises(ValueError):
            parse_bool(x, **kwds)
    else:
        res = parse_bool(x, **kwds)
        assert res == exp
