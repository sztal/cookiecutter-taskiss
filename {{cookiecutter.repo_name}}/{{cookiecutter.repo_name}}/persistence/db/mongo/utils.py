"""*MongoDB* / *Mongoengine* related utilities.

See Also
--------
pymongo
mongoengine
"""
from collections import Iterable


def update_action_hook(doc, hook='$set', processor=None):
    """Action hook for transforming document into `$set` update statements.

    Parameters
    ----------
    doc : dct
        Valid *MongoDB* document object.
    hook : str
        Valid *MongoDB* action hook like `$set` or `$push`.
    processor: func or None
        Optional processor function to transform the document.
    """
    action = { hook: doc }
    if processor:
        action[hook] = processor(action[hook])
    return action

def query_factory(query_or_fields):
    """Query function factory."""
    if callable(query_or_fields):
        return query_or_fields
    if isinstance(query_or_fields, str) or not isinstance(query_or_fields, Iterable):
        query_or_fields = [query_or_fields]
    def query(dct):
        return { f: dct.pop(f) for f in query_or_fields }
    return query
