"""Tasks definitions.

Attributes section describe additional attributes that may be defined
on tasks.

Attributes
----------
dependson : list or tuple of str
    List of task names that the task depends on
noargs : bool
    Should task be run with immutable signature if chained.
"""
import time
from {{ cookiecutter.repo_name }} import taskiss

# Set of example tasks with complex dependency graph --------------------------

cfg_schema = {
    'cfg': {
        'type': 'dict',
        'schema': {
            't1': { 'type': 'number', 'coerce': int },
            't2': { 'type': 'number', 'coerce': int },
            't3': { 'type': 'list', 'schema': { 'type': 'string'} }
        }
    }
}

@taskiss.task(ignore_result=False, _interface={
    'cfg': { 'type': 'dict' }
})
def cfg(cfg):
    return { 'cfg': cfg }

@taskiss.task(dependson=[__name__+'.cfg'], ignore_result=False, _interface=cfg_schema)
def t1(cfg):
    return { 'x': cfg.get('t1', 0) }

@taskiss.task(dependson=[__name__+'.cfg'], ignore_result=False, _interface=cfg_schema)
def t2(cfg):
    time.sleep(1)
    return { 'y': cfg.get('t2', 0) }

@taskiss.task(dependson=[__name__+'.cfg'], ignore_result=False, _interface=cfg_schema)
def t3(cfg):
    return { 'strings': cfg.get('t3') }

@taskiss.task(dependson=[__name__+'.t3'], ignore_result=False, _interface={
    'strings': {
        'type': 'list',
        'schema': { 'type': 'string' }
    }
})
def t4(strings):
    time.sleep(1)
    return { 'path': " => ".join(strings) }

@taskiss.task(dependson=[__name__+'.t1', __name__+'.t2'], ignore_result=False, _interface={
    'x': { 'type': 'number', 'coerce': int },
    'y': { 'type': 'number', 'coerce': int }
})
def t5(x, y):
    return { 'n': x * y }

@taskiss.task(dependson=[__name__+'.t5', __name__+'.t4'], ignore_result=False, _interface={
    'path': { 'type': 'string' },
    'n': { 'type': 'number', 'coerce': int }
})
def t6(path, n):
    time.sleep(1)
    return { 'path': "[{}] {}".format(n, path) }

@taskiss.task(dependson=[__name__+'.t6'], ignore_result=False, _interface={
    'path': { 'type': 'string' }
})
def t7(path):
    return path

@taskiss.task(ignore_result=False, _interface={
    'x': { 'type': 'integer', 'min': 0, 'coerce': int }
})
def long_task(x):
    time.sleep(x)
    return True

@taskiss.task(_interface={})
def very_long_task():
    time.sleep(60*60)
    return True
