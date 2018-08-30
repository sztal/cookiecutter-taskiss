"""Base item and item loader classes."""
from scrapy.loader import ItemLoader
from scrapy.loader.processors import TakeFirst, MapCompose
from .utils import normalize_web_content, strip

class BaseItemLoader(ItemLoader):
    """Base item loader class.

    It defines helper method used for initializing instances
    of specialized subclasses.
    """
    default_item_class = None
    default_input_processor = MapCompose(normalize_web_content, strip)
    default_output_processor = TakeFirst()

    # Selectors
    container_sel = None

    # Methods -----------------------------------------------------------------

    def __init__(self, *args, **kwds):
        """Initilization method.

        Parameters
        ----------
        omit : list of str
            List of fields to omit.
        """
        super().__init__(*args, **kwds)
        self._container = None

    @property
    def fields(self):
        """Fields getter."""
        if self.default_item_class is None:
            cn = self.__class__.__name__
            raise AttributeError(f"'{cn}' does not define 'default_item_class' attribute")
        return [ f for f in self.default_item_class.fields ]

    def assign_container_selector(self):
        """Assign container selector."""
        if self.container_sel is None:
            cn = self.__class__.__name__
            raise AttributeError(f"'{cn}' does not define 'container_sel' attribute")
        selector, selector_type = self.container_sel
        if selector_type == 'xpath':
            self._container = self.nested_xpath(selector)
        elif selector_type == 'css':
            self._container = self.nested_css(selector)
        else:
            raise ValueError("Unknown selector type: {}".format(selector_type))

    def assign_selector(self, field_name, selector_name=None):
        """Assign selector to a field.

        Parameters
        ----------
        field_name : str
            Field name.
        selector_name : str
            Selector name. May not have the 'sel_' prefix.
        """
        if not selector_name:
            selector_name = field_name+'_sel'
        selector_spec = getattr(self, selector_name, None)
        if selector_spec is None:
            return
        selector, selector_type = selector_spec
        if selector_type == 'xpath':
            self._container.add_xpath(field_name, selector)
        elif selector_type == 'css':
            self._container.add_css(field_name, selector)
        else:
            raise ValueError(f"Unknown selector type: {selector_type}")

    def setup(self, omit=()):
        """Setup loader selectors.

        Parameters
        ----------
        omit : list of str
            List of fields to omit.
        """
        self.assign_container_selector()
        for field in self.fields:
            if field in omit:
                continue
            self.assign_selector(field)

    def add_data(self, data):
        """Add response (meta)data.

        Parameters
        ----------
        data : dict-like
            Metadata obtained from the response-request.
        """
        self.data = data
