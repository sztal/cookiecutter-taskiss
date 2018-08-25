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
from {{ cookiecutter.repo_name }}.taskiss import taskiss
