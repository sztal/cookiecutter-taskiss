"""Base item and item loader classes."""
from scrapy.loader import ItemLoader
from scrapy.loader.processors import TakeFirst, MapCompose
from {{ cookiecutter.repo_name }}.webscraping.utils import normalize_web_content
from {{ cookiecutter.repo_name }}.utils.string import strip

class BaseItemLoader(ItemLoader):
    """Base item loader class.

    It defines helper method used for initializing instances
    of specialized subclasses.
    """
    default_input_processor = MapCompose(normalize_web_content, strip)
    default_output_processor = TakeFirst()

    # Selectors
    sel_container = (None, None)

    # Methods -----------------------------------------------------------------

    def __init__(self, *args, **kwds):
        """Initilization method."""
        super().__init__(*args, **kwds)
        self._container = None

    def assign_container_selector(self):
        """Assign container selector."""
        selector, selector_type = self.sel_container
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
            selector_name = field_name
        if not selector_name.startswith('sel_'):
            selector_name = 'sel_'+selector_name
        for sname in [ a for a in dir(self) if a.startswith(selector_name) ]:
            selector_spec = getattr(self, sname)
            if selector_spec is None:
                return
            selector, selector_type = selector_spec
            if selector_type == 'xpath':
                self._container.add_xpath(field_name, selector)
            elif selector_type == 'css':
                self._container.add_css(field_name, selector)
            else:
                raise ValueError("Unknown selector type: {}".format(selector_type))

    def setup(self):
        """Setup loader selectors."""
        self.assign_container_selector()
