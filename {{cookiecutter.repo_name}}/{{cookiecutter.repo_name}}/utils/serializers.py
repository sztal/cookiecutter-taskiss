"""Serializer and deserializer functions and classes."""
# pylint: disable=E0202
from datetime import datetime, date
from json import JSONEncoder
from scrapy import Item


class SmartJSONEncoder(JSONEncoder):
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
