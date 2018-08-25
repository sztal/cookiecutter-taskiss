"""Test cases for :py:mod:`{{ cookiecutter.repo_name }}.meta`."""
import re
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
        self.setcomponents([
            ('somey', Something(x))
        ])

class SomeClass(ParentClass, metaclass=Composable):
    """Some class with both class- and instance-level components."""
    __components = [
        ('regex', re.compile(r"foo", re.IGNORECASE))
    ]

    def __init__(self, pattern):
        """Instance-level components defined at runtime."""
        self.setcomponents([
            ('rx', re.compile(pattern, re.IGNORECASE))
        ])


class TestComposable:
    """Test cases for
    :py:class:`{{ cookiecutter.repo_name }}.meta.Composable`.
    """
    def test_simple(self):
        """Simple test case."""
        inst = SomeClass(r"bar")
        assert hasattr(inst, 'regex')
        assert 'regex' in dir(inst)
        assert hasattr(inst, 'rx')
        assert 'rx' in dir(inst)
        assert inst.regex == re.compile(r"foo", re.IGNORECASE)
        assert inst.rx == re.compile(r"bar", re.IGNORECASE)
        assert inst.search("bar") is not None
        assert inst.search("foo") is None
        assert '__components' in dir(inst)
        assert '_SomeClass__components' in dir(inst)


    def test_complex(self):
        """Complex test case."""
        inst = SomeClass(r"bar")
        assert hasattr(inst, 'somex')
        assert 'somex' in dir(inst)
        assert not hasattr(inst, 'somey')
        assert 'somey' not in dir(inst)
        assert hasattr(inst, 'meth')
        assert 'meth' not in dir(inst)
        assert inst.meth() == 10
        assert '_ParentClass__components' in dir(inst)
