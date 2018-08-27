"""Spider base and component classes."""
# pylint: disable=E1101,W0221,W0223
import json
import pdb
import hashlib
from logging import getLogger
from scrapy import Spider, Request
from scrapy.http import HtmlResponse
from scrapy_splash import SplashRequest, SplashJsonResponse
from w3lib.url import canonicalize_url
from {{ cookiecutter.repo_name }}.config import cfg, MODE
from {{ cookiecutter.repo_name }}.utils.processors import parse_bool
from {{ cookiecutter.repo_name }}.base.interface import ScrapyCLIExtraArgsInterface


class BaseSpider(Spider):
    """Base spider class.

    It defines default methods and class attributes,
    but is not usable as such, that is, it must be subclassed,
    as it does not have neither the `name` attributes nor the `parse` method.

    All subclasses must define `get_urls` in order to generate requests.

    Attributes
    ----------
    limit : int or None
        Limit for number of requests being made.
    mode : str or None
        Special mode the spider is run in.
        Currently only value `debug` is supported and it set a `pdb`
        breakpoint in the parse method right before the return statement.
    storage : str or None
        Type of storage used for data persistence.
        If `None` then both disk and database storage is used.
        Value `all` is an alias for `None`.
        If it is `nodb` the only disk persistence is used.
        If it is `no` then no persistence is used.
        Other values raise `ValueError`.
    allowed_domains : list of str
        This is a standard `scrapy` spider class attribute, but it is documented
        here as it has an additional meaning: the provided domains are used
        to filter out also starting responses (those generated from `start_urls`)
        if their final URLs (after redirects etc.) are not in the specified
        domains.
    start_urls_allowed_domains : list of str
        List of accepted domains used for filtering the `start_urls`.
        This is useful when one want to give a lot of start URLs and make
        the spider care for selecting only the proper ones.
    overwrite : bool or None
        If `True` then data for given source is deleted before running the spider.
    blacklist_urls : list of str or SRE_Pattern or None
        List of urls or compiled regexps for filtering unwanted urls.
        Used in the `OffsiteFinalUrlDownloaderMiddleware`.
    test_url : str or None
        Single url to fetch and parse. Meant for testing purposes.
    hashing_salt : str or None
        Salt added when hashing sensitive text data (like usernames).
        For sake of reproducibility it should be config based instead of
        purely random.

    Notes
    -----
    Spider behaviour may be modified by additional command-line arguments
    that are described in this docstring and also in
    :py:class:`{{ cookiecutter.repo_name }}.base.interface.ScrapyCLIExtraArgsInterface`.
    The arguments are not injected into a spider object directly, but are stored
    in wrapped object in `spider.args`.
    """
    limit = None
    mode = None
    storage = None
    overwrite = False
    test_url = None
    hashing_salt = cfg.get(MODE, 'web_user_salt')

    # Allowed values for extra attributes
    _storage_values = [ None, 'all', 'no', 'nodb' ]
    _mode_values = [ None, 'debug' ]

    logger = getLogger('scrapy')

    # Spider-level scrapy settings
    custom_settings = {
        'ITEM_PIPELINES': {
            'smcore.web.pipelinecls.BaseSpiderItemPipeline': 300
        }
    }

    # Methods -----------------------------------------------------------------

    @classmethod
    def parse_extra_args(cls):
        """Consume extra args and place them in a wrapper object."""
        args = {}
        for key in ScrapyCLIExtraArgsInterface.schema.schema:
            if hasattr(cls, key):
                args[key] = getattr(cls, key)
                delattr(cls, key)
        cls.args = ScrapyCLIExtraArgsInterface(**args)

    def get_urls(self):
        """Get urls and request data from the database.

        Returns
        -------
        iterable
            Iterable of 2-tuple where first element is request url
            and second a dict with additional request metadata.
            Second element is not used if it is falsy.
        """
        raise NotImplementedError(
            "Subclass does not define the abstract `get_urls` method"
        )

    def start_requests(self):
        """Generate start requests."""
        self.parse_extra_args()
        if self.test_url:
            urls = [ (self.test_url, { 'link': self.test_url }) ]
        else:
            urls = self.get_urls()
        n = 0
        for url, data in urls:
            n += 1
            if self.limit and n > self.limit:
                break
            request = self.make_request(url, meta={ 'data': data })
            yield request

    def make_request(self, url, **kwds):
        """Make request object.

        Parameters
        ----------
        url : str
            Request url.
        **kwds :
            Parameters passed to `scrapy.Request` constructor.

        Returns
        -------
        scrapy.Request
            A request object.
        """
        request = Request(url, **kwds)
        return request

    def hash_string(self, string, salt=None):
        """Get MD5 hash from a string.

        Parameters
        ----------
        string : str
            Some string.
        salt : str, False or None
            Salt added to the string for additional obfuscation.
            No salting if `False`, class-level salt if `None`.
            Otherwise provided salt is added.
        """
        if salt is None:
            salt = self.hashing_salt
        if isinstance(salt, str):
            string += salt
        return hashlib.md5(string.encode('utf-8')).hexdigest()


class SplashSpider(BaseSpider):
    """Extension of
    :py:class:`{{ cookiecutter.repo_name }}.webscraping.spidercls.BaseSpider`
    for crawling pages with dynamic js content.

    Attributes
    ----------
    lua_source : str or None
        Lua script defining in-browser actions to perform before rendering
        scrapy-splash response. Used only if splash is `True`.
    """
    lua_source = None

    # Spider-level scrapy settings
    custom_settings = BaseSpider.custom_settings.update({
        'DOWNLOADER_MIDDLEWARES': {
            'scrapy_splash.SplashCookiesMiddleware': 723,
            'scrapy_splash.SplashMiddleware': 725,
            'scrapy.downloadermiddlewares.httpcompression.HttpCompressionMiddleware': 810
        },
        'SPIDER_MIDDLEWARES': {
            'scrapy_splash.SplashDeduplicateArgsMiddleware': 100
        },
        'DUPEFILTER_CLASS': 'scrapy_splash.SplashAwareDupeFilter',
        'HTTPCACHE_STORAGE': 'scrapy_splash.SplashAwareFSCacheStorage'
    })

    # Methods -----------------------------------------------------------------

    def make_request(self, url, args=None, **kwds):
        """Make splash-aware request object.

        Parameters
        ----------
        url : str
            Request url.
        args : dict or None
            Additional splash arguments.
        **kwds :
            Parameters passed to `scrapy.Request` constructor.

        Returns
        -------
        scrapy.Request
            A request object.
        """
        args = {} if args is None else args
        if self.lua_source:
            args.update(lua_source=self.lua_source)
            kwds.update(
                endpoint='execute',
                args=args
            )
        else:
            kwds.update(endpoint='render.html')
        request = SplashRequest(url=url, **kwds)
        return request

    def parse(self, response):
        """Parse method."""
        if isinstance(response, SplashJsonResponse):
            data = json.loads(response.body_as_unicode())
            body = data['src']
            url = data.get('final_url', response.url)
            response = HtmlResponse(
                url=url,
                body=body,
                encoding='utf-8',
                request=response.request
            )
        return super().parse(response)
