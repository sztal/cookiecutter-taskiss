"""Test cases for :py:module:`{{ cookiecutter.repo_name }}.meta`."""
import re
import pytest
from {{ cookiecutter.repo_name }}.meta import Composable


class Something(object):
    """Some dummy class."""
    def __init__(self, x):
        self.x = x

    def meth(self):
        """And dummy method."""
        return self.x

class ParentClass(metaclass=Composable):
    """Parent composable class."""
    __components = [
        ('somex', Something(10))
    ]

    def __init__(self, x):
        """Initialization method."""
        self.setcomponents_([
            ('somey', Something(x))
        ])

class SomeClass(ParentClass, metaclass=Composable):
    """Some class with both class- and instance-level components."""
    __components = [
        ('regex', re.compile(r"foo", re.IGNORECASE))
    ]

    def __init__(self, pattern):
        """Instance-level components defined at runtime."""
        self.setcomponents_([
            ('rx', re.compile(pattern, re.IGNORECASE))
        ])

@pytest.fixture
def some_instance():
    return SomeClass(r"bar")


class TestComposable:
    """Test cases for
    :py:class:`{{ cookiecutter.repo_name }}.meta.Composable`.
    """
    def test_simple(self, some_instance):
        """Simple test case."""
        assert hasattr(some_instance, 'regex')
        assert 'regex' in dir(some_instance)
        assert hasattr(some_instance, 'rx')
        assert 'rx' in dir(some_instance)
        assert some_instance.regex == re.compile(r"foo", re.IGNORECASE)
        assert some_instance.rx == re.compile(r"bar", re.IGNORECASE)
        assert some_instance.search("bar") is not None
        assert some_instance.search("foo") is None
        assert '__components' in dir(some_instance)
        assert '_SomeClass__components' in dir(some_instance)

    def test_complex(self, some_instance):
        """Complex test case."""
        assert hasattr(some_instance, 'somex')
        assert 'somex' in dir(some_instance)
        assert not hasattr(some_instance, 'somey')
        assert 'somey' not in dir(some_instance)
        assert hasattr(some_instance, 'meth')
        assert 'meth' not in dir(some_instance)
        assert some_instance.meth() == 10
        assert '_ParentClass__components' in dir(some_instance)

    def test_getcomponents_and_getattribute(self, some_instance):
        """Test case for 'getcomponents_` and `getattribute_` methods."""
        search1 = some_instance.getcomponents_('SomeClass')['regex'].search
        search2 = some_instance.getattribute_('search', 'regex', 'SomeClass')
        search3 = some_instance.regex.search
        rx_search = some_instance.search
        assert search1 == search2 == search3
        assert search1 != rx_search
        with pytest.raises(AttributeError):
            some_instance.getattribute_('search', 'regex')
        with pytest.raises(AttributeError):
            some_instance.getcomponent_('regex')

    def test_setattribute_instance(self, some_instance):
        """Test case for `setattribute_` method."""
        some_instance.setattribute_('regex', 'foo', on_component=False)
        regex1 = some_instance.regex
        regex2 = some_instance.getcomponent_('regex', 'SomeClass')
        assert regex1 != regex2

    def test_setattribute_component(self, some_instance):
        """Test case for `setattribute_` method."""
        some_instance.setattribute_('x', 'foo', on_component=True)
        x1 = some_instance.x
        x2 = some_instance.getattribute_('x', 'somex', 'ParentClass')
        assert x1 == x2
