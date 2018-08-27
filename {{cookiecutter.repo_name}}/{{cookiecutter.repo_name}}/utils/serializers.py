"""Serializer and deserializer functions and classes."""
# pylint: disable=E0202
from datetime import datetime, date
from json import JSONEncoder as _JSONEncoder
from json import JSONDecoder as _JSONDecoder
from scrapy import Item


class JSONEncoder(_JSONEncoder):
    """JSON serializer handling :py:class:`datetime.datetime` objects.

    It also serializes :py:class:`scrapy.Item` instances.
    """
    def default(self, o):
        """Serializer method."""
        if isinstance(o, (date, datetime)):
            return o.isoformat()
        if isinstance(o, Item):
            return dict(o)
        return super().default(o)


class UniversalJSONEncoder(JSONEncoder):
    """Universal JSON encoder.

    It tries to dump all non-serializable objects
    (other than thos handled by
    :py:class:`{{ cookiecutter.repo_name }}).utils.serializers.JSONEncoder`)
    to their standard string representation.
    """
    def default(self, o):
        """Seralizer method."""
        try:
            return super().default(o)
        except TypeError:
            return str(o)
