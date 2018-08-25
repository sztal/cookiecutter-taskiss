"""*MongoDB* / *Mongoengine* related utilities.

See Also
--------
pymongo
mongoengine
"""
# pylint: disable=W0212
from collections import Iterable
from pymongo import UpdateOne, UpdateMany


def action_hook_set(doc, hook='$set', processor=None):
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

def make_update_op(doc, query_fields, multiple=False, upsert=True,
                   action_hook=action_hook_set, **kwds):
    """Make PyMongo update op.

    Parameters
    ----------
    query_fields : str or list of str
        Field names to perform document query.
    action_hook : func
        MongoDB update action hook.
    upsert : bool
        Should upsert be done instead of update.
    **kwds :
        Parameters passed to `pymongo.UpdateOne` or `pymongo.UpdateMany`.
    """
    if isinstance(query_fields, str) or not isinstance(query_fields, Iterable):
        query_fields = [ query_fields ]
    if 'upsert' not in kwds:
        kwds.update(upsert=upsert)
    query = { f: doc.pop(f) for f in query_fields }
    update = action_hook(doc)
    if multiple:
        op = UpdateMany(query, update, **kwds)
    else:
        op = UpdateOne(query, update, **kwds)
    return op

def make_bulk_update(data, query_fields, model, bulk_write_kwds=None, **kwds):
    """Make bulk update.

    Parameters
    ----------
    query_fields : str or list of str
        Field names used in document query.
    data : list-like object of dict-like records
        Records to update. Must provide `pop` method.
    model : odm model
        ODM model to update.
    bulk_write_kwds : dict or None
        Arguments passed to :py:function:`pymongo.bulk_write`.
        If `None` then `ordered=False` is passed.
    **kwds :
        Other arguments passed to `make_update_op`.
    """
    if bulk_write_kwds is None:
        bulk_write_kwds = { 'ordered': False }
    bulk_ops = []
    while data:
        op = make_update_op(data.pop(), query_fields, **kwds)
        bulk_ops.append(op)
    if bulk_ops:
        model._get_collection().bulk_write(bulk_ops, **bulk_write_kwds)
