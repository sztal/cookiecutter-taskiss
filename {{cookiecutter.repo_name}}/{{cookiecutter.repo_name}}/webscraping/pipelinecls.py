"""Item pipeline base and component classes."""
# pylint: disable=E1101,W0613
import json
from {{ cookiecutter.repo_name }}.utils.path import get_persistence_path
from {{ cookiecutter.repo_name }}.meta import Composable


class BaseSpiderItemPipeline(metaclass=Composable):
    """Base spider item pipeline class.

    This class handles both disk persistence (writing scraped items to .jl files)
    and db persistence (saving scraped data in the database).
    This is accomplished through persistence component classes.
    """
    disk_persistence_kwds = {}
    db_persistence_kwds = {}

    # Methods -----------------------------------------------------------------

    def __init__(self,  disk_persistence_cls, db_persistence_cls,
                 disk_persistence_kwds=None, db_persistence_kwds=None):
        """Initialization method.

        Parameters
        ----------
        disk_persistence_kwds : dict or None
            Keyword arguments passed to disk persistence object.
            Use class attribute if `None`.
        db_persistence_kwds : dict or None
            Keyword arguments passed to db persistence object.
            Use class attribute if `None`.
        """
        if disk_persistence_kwds is None:
            disk_persistence_kwds = self.disk_persistence_kwds
        if db_persistence_kwds is None:
            db_persistence_kwds = self.db_persistence_kwds
        self.setcomponents_([
            ('disk_persistence', disk_persistence_cls(**disk_persistence_kwds))
            ('db_persistence', db_persistence_cls(**db_persistence_kwds))
        ])

    def open_spider(self, spider):
        """Pipeline opening hook."""
        if not self.filename:
            self.setattribute_('filename', spider.name+'-{}.jl')
        self.disk_persistence._set_attributes(filename=self.filename)
        # Remove source data if `overwrite` mode is on
        if spider.overwrite:
            self.overwrite_storage(spider)

    def overwrite_storage(self, spider):
        """Overwrite storage."""
        raise NotImplementedError("'{}' does not define 'overwrite_storage' method".format(
            self.__class__.__name__
        ))

    def process_item(self, item, spider):
        """Item processing hook."""
        if spider.storage is None or spider.storage != 'no':
            self.disk_persistence.persist(item, print_num=False)

    def close_spider(self, spider):
        """Pipeline closing hook."""
        if spider.storage is None:
            with open(self.disk_persistence.filepath, 'r') as f:
                with self.db_persistence:
                    for line in f:
                        doc = json.loads(line.strip())
                        self.db_persistence.persist(doc)
