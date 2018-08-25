"""Metaprogramming utilities.

This module provide a set of various metaprogramming utilities
such as general purpose metaclasses, mixins and decorators.
"""
# pylint: disable=W0613,W0212
from functools import singledispatch, update_wrapper

# Decorators ------------------------------------------------------------------

def methdispatch(func):
    """Single dispatch for instance methods."""
    dispatcher = singledispatch(func)
    def wrapper(*args, **kwds):
        """Internal wrapper."""
        return dispatcher.dispatch(args[1].__class__)(*args, **kwds)
    wrapper.register = dispatcher.register
    update_wrapper(wrapper, func)
    return wrapper

# Metaclasses -----------------------------------------------------------------

def __getattr__(self, attr):
    """Attribute lookup for composable classes."""
    components_attr = '_'+self.__class__.__name__+'__components'
    components = getattr(self, components_attr, [])
    bases = (self.__class__, *self.__class__.__bases__)
    for base in bases:
        components_attr = '_'+base.__name__+'__components'
        components = [ *components, *getattr(base, components_attr, []) ]
    for nm, component in components:
        if nm == attr:
            return component
        try:
            return getattr(component, attr)
        except AttributeError:
            pass
    msg = "'{}' object has no attribute '{}'".format(self.__class__.__name__, attr)
    raise AttributeError(msg)


class Composable(type):
    """Metaclass for injecting easy class composition functionality.

    Class components may be defined on two different level:
    class level and instance level.

    In both cases they are defined based on a private class/instance
    attribute `__components`, and this name automatically expands to
    `_<classname>__components`. In both cases `__component` attribute
    must be a tuple of 2-tuples providing name (str) and component instance.
    Automatic name expansion does not matter as the metaclass extends the
    standard `__getattr__` method that solves this problem.

    Injected components may be accessed as standard attributes using the
    provided names. Moreover, all attributes of injected components
    also became accessible in the standard fashion. However, it should be
    noted that the order of specification of components matter in the case
    when multiple components define the same attribute.

    Also method delegation order is important, as first instance level
    components will be searched and then class level components in
    the standard order.

    Notes
    -----
    Differentiation between instance and class level components
    is useful, as it allow to define components available only for
    specific instances and which may be initialized in runtime
    within the host object `__init__` method.
    """
    def __new__(cls, name, bases, namespace, **kwds):
        """Class instance constructor."""
        newclass = super().__new__(cls, name, bases, namespace)
        setattr(newclass, __getattr__.__name__, __getattr__)
        components_attr = '_'+newclass.__name__+'__components'
        for nm, component in getattr(newclass, components_attr, []):
            if hasattr(newclass, nm):
                errmsg = "Class '{}' already has attribute '{}'".format(
                    newclass.__name__, nm
                )
                raise AttributeError(errmsg)
            setattr(newclass, nm, component)
        return newclass
