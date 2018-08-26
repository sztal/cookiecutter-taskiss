"""*MongoDB* / *Mongoengine* related utilities.

See Also
--------
pymongo
mongoengine
"""
# pylint: disable=W0212
from collections import Iterable
from pymongo import UpdateOne, UpdateMany


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
