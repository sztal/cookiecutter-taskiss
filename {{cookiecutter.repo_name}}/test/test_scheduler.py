"""Test _Scheduler_ class."""
import pytest
from {{ cookiecutter.repo_name }}.taskiss.{{ cookiecutter.taskmodule_name }} import cfg


@pytest.mark.task
def test_execute_task(scheduler):
    res = scheduler.execute_task(cfg, cfg={
        't1': 10,
        't2': 20,
        't3': ['a', 'b', 'c']
    }, propagate=True)
    res = [ r.get() for r in res ]
    exp = [
        { 'cfg': { 't1': 10, 't2': 20, 't3': [ 'a', 'b', 'c' ] } },
        { 'strings': [ 'a', 'b', 'c' ] },
        { 'path': 'a => b => c' },
        { 'y': 20 },
        { 'x': 10 },
        { 'n': 200 },
        { 'path': '[200] a => b => c' },
        { '_args': [ '[200] a => b => c' ] }
    ]
    assert res == exp
