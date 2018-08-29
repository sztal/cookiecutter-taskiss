"""CLI: DB submodule for MongoDB / Mongoengine management."""
# pylint: disable=W0212
import json
import click
from ..utils import eager_callback, pprint, parse_args, to_console
from .utils import get_mongo_model
from .utils import show_mongo_models, show_mongo_model_schema


@click.group()
@click.option('--show-models', is_flag=True, default=False, expose_value=False,
              is_eager=True, callback=eager_callback(show_mongo_models))
def mongo():
    """MongoDB / Mongoengine management inteface."""
    pass

@mongo.command(name='schema', help="Show schema of a MongoDB model.")
@click.argument('path_or_name', nargs=1, type=str)
def _(path_or_name):
    """Show schema of a MongoDB object.

    Main argument must be a proper python path or a simple class name.
    """
    show_mongo_model_schema(path_or_name)

@mongo.command(name='find', help="Run a find query against a MongoDB collection.")
@click.argument('path_or_name', nargs=1, type=str, required=True)
@click.argument('query', nargs=1, type=str, required=True)
@click.option('--field', '-f', type=str, multiple=True,
              help="Field names to limit to the results.")
@click.option('--exclude', is_flag=True, default=False,
              help="Should selected fields be excluded instead of included.")
@click.option('--limit', '-l', type=int, help="Limit printed results.")
@click.option('--skip', '-s', type=int, help="Skip first *n* documents.")
@click.option('--order', '-o', type=str, multiple=True,
              help="Sort by fields (multiple allowed). Set to '-field_name' to sort descending.")
@click.option('--dry', is_flag=True, default=False,
              help="Dry run: only show how the engine interprets the query.")
def _(path_or_name, query, field, exclude, limit, skip, order, dry):
    """Run a find query against a MongoDB collection.

    Notes
    -----
    Add the moment the interface does not support usage of regexp in queries.
    """
    query = json.loads(query)
    if dry:
        pprint(query)
        return
    model = get_mongo_model(path_or_name)
    s = slice(None, None)
    if limit and skip:
        s = slice(skip, limit)
    elif limit:
        s = slice(limit)
    elif skip:
        s = slice(4, None)
    if exclude:
        cursor = model.objects(__raw__=query).exclude(*field).order_by(*order)[s]
    else:
        cursor = model.objects(__raw__=query).only(*field).order_by(*order)[s]
    for doc in cursor:
        if exclude:
            doc = doc.to_dict(*field, ignore_fields=False)
        else:
            doc = doc.to_dict(only=field)
        pprint(doc)

@mongo.command(name='remove', help="Remove documents from MongoDB collection.")
@click.argument('path_or_name', nargs=1, type=str)
@click.argument('query', nargs=1, type=str, required=True)
@click.option('--parg', '-p', type=str, multiple=True,
              help="Additional arguments for MongoDB 'remove' method. Parsed as JSON.")
@click.option('--dry', is_flag=True, default=False,
              help="Dry run: only show how the engine interprets the query.")
def _(path_or_name, query, parg, dry):
    """Run remove query against a MongoDB collection."""
    query = json.loads(query)
    if dry:
        pprint(query)
        return
    model = get_mongo_model(path_or_name)
    kwds = parse_args(*parg, parser='json')
    res = model.objects(__raw__=query).delete(write_concern=kwds)
    pprint(res)

@mongo.command(name='update', help="Update documents in MongoDB collection.")
@click.argument('path_or_name', nargs=1, type=str)
@click.argument('query', nargs=1, type=str)
@click.argument('update', nargs=1, type=str)
@click.option('--upsert/--not-upsert', default=False,
              help="Should upsert mode be used.")
@click.option('--multiple/--not-multiple', default=True,
              help="Allow updating multiple documents.")
@click.option('--parg', '-p', multiple=True,
              help="Additional named arguments parsed as JSON strings.")
@click.option('--dry', is_flag=True, default=False,
              help="Dry run: only show how the engine interprets the query.")
def _(path_or_name, query, update, upsert, multiple, parg, dry):
    """Update documents in MongoDB collection."""
    query = json.loads(query)
    update = json.loads(update)
    if dry:
        for doc in [ query, update ]:
            pprint(doc)
        return
    coll = get_mongo_model(path_or_name)._get_collection()
    kwds = parse_args(*parg, parser='json')
    if multiple:
        res = coll.update_many(query, update, **kwds)
    else:
        res = coll.update_one(query, update, **kwds)
    return res

@mongo.command(name='aggregate', help="Run an aggregate query againt a MongoDB collection.")
@click.argument('path_or_name', nargs=1, type=str, required=True)
@click.argument('pipeline', nargs=-1, type=str, required=True)
@click.option('--arg', '-a', type=str, multiple=True,
              help="Args passed to the task (i.e. -a x=10).")
@click.option('--parg', '-p', type=str, multiple=True,
              help="Literal evaluated args passed to the task (i.e. -e x=['a']).")
@click.option('--dry', is_flag=True, default=False,
              help="Dry run: only show how the engine interprets the query.")
def _(path_or_name, pipeline, arg, parg, dry):
    """Run an aggregate query against a collection.

    Additional keyword arguments are used to configure the aggregation process.
    Pipeline stages are specified as positional arguments following the
    collection class path/name.
    """
    pipeline = [ json.loads(stage) for stage in pipeline ]
    if dry:
        to_console(pipeline)
        return
    model = get_mongo_model(path_or_name)
    kwds = { **parse_args(*arg), **parse_args(*parg, parser='json') }
    cursor = model.objects.aggregate(*pipeline, **kwds)
    for doc in cursor:
        pprint(doc)

@mongo.command(name='drop', help="Drop MongoDB collection.")
@click.argument('path_or_name', nargs=1, type=str)
def _(path_or_name):
    """Drop MongoDB collection represented by a model class."""
    model = get_mongo_model(path_or_name)
    cname = model._get_collection_name()
    click.confirm(
        f"Are you sure you want drop '{cname}' collection? This can not be undone.",
        abort=True
    )
    model.drop_collection()
    click.echo(f"Collection '{cname}' has been dropped.")
