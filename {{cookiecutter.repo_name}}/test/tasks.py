"""Test tasks."""
import time
from {{ cookiecutter.repo_name }}.taskiss import taskiss
from {{ cookiecutter.repo_name }}.taskiss.taskcls import TaskissTask

# Set of tasks with complex dependency graph ----------------------------------

@taskiss.task(ignore_result=False)
def cfg(cfg, **kwds):
    return { 'cfg': cfg }

@taskiss.task(dependson=[__name__+'.cfg'], ignore_result=False)
def t1(cfg, **kwds):
    time.sleep(1)
    return { 'x': cfg.get('t1', 0) }

@taskiss.task(dependson=[__name__+'.cfg'], ignore_result=False)
def t2(cfg, **kwds):
    time.sleep(1)
    return { 'y': cfg.get('t2', 0) }

@taskiss.task(dependson=[__name__+'.cfg'], ignore_result=False)
def t3(cfg, **kwds):
    time.sleep(1)
    return { 'strings': cfg.get('t3') }

@taskiss.task(dependson=[__name__+'.t3'], ignore_result=False)
def t4(strings, **kwds):
    time.sleep(1)
    return { 'path': " => ".join(strings) }

@taskiss.task(dependson=[__name__+'.t1', __name__+'.t2'], ignore_result=False)
def t5(x, y, **kwds):
    time.sleep(1)
    return { 'n': x * y }

@taskiss.task(dependson=[__name__+'.t5', __name__+'.t4'], ignore_result=False)
def t6(path, n, **kwds):
    time.sleep(1)
    return { 'path': "[{}] {}".format(n, path) }

@taskiss.task(dependson=[__name__+'.t6'], ignore_result=False)
def t7(path, **kwds):
    time.sleep(1)
    return path
