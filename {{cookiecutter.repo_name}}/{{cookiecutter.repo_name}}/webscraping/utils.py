"""Web and webscraping related utilities.

This module also contain processors that for sake of avoiding circular imports
can not be placed in `misc.processors`.
"""
from scrapy.http import HtmlResponse
from w3lib.html import remove_tags, remove_comments, strip_html5_whitespace
from w3lib.html import replace_entities, replace_escape_chars, replace_tags
import tldextract as tld
from {{ cookiecutter.repo_name }}.cfg import cfg, MODE
from {{ cookiecutter.repo_name }}.textprocessing import hash_string

USER_SALT = cfg.get(MODE, 'web_user_salt')


def get_url_domain(url):
    """Get domain from an URL.

    Parameters
    ----------
    url : str
        URL.
    """
    return '.'.join([ p for p in tld.extract(url)[-2:] if p ])

def is_url_in_domains(url, domains):
    """Check if URL is in domain(s).

    Parameters
    ----------
    url : str
        URL.
    domains : str or iterable of str
        Domains to be checked.
    """
    if not domains:
        return True
    if isinstance(domains, str):
        domains = [ domains ]
    return get_url_domain(url) in domains

def normalize_web_content(x, keep=('h2', 'h3', 'h4', 'h5', 'h6', 'strong'),
                          token='____SECTION____'):
    """Normalize web content.

    Parameters
    ----------
    keep : tuple
        HTML tags to keep.
    token : str or None
        Token to use for replacing kep HTML tags.
        Do not replace if `None`.
    """
    try:
        x = strip_html5_whitespace(x)
        x = remove_comments(x)
        x = remove_tags(x, keep=keep)
        if token:
            x = replace_tags(x, token=token)
        x = replace_entities(x)
        x = replace_escape_chars(x)
    except (TypeError, AttributeError):
        pass
    return x

def hash_user(string):
    """Hash username.

    Username is salted with the salt defined in the config.

    Parameters
    ----------
    string : str
        Username.
    """
    return hash_string(string, salt=USER_SALT)

def load_item(body, item_loader, item=None, url='placeholder_url',
              callback=None, encoding='utf-8'):
    """Load item from HTML string.

    Parameters
    ----------
    body : str
        String with valid HTML markup.
    item_loader : BaseItemLoader
        Item loader class sublassing the `BaseItemLoader` defined in `items.py`.
    item : scrapy.Item
        Optional item class to be used instead of the `item_loader` default.
    url : str
        Optional url to pass to the response.
        For most of cases it shoul left as it is.
    callback : func
        Optional callback function to perform on item loader after setup.
        Call back should not return any value,
        but only modify the state of the loader.
        This meant mostly to use additional setup methods
        defined on a given item loader class.
    encoding : str
        Response encoding. Defaults to UTF-8.

    Returns
    -------
    scrapy.Item
        Item object populated with data extracted from the HTML markup.
    """
    response = HtmlResponse(url=url, body=body, encoding=encoding)
    if item:
        loader = item_loader(item=item(), response=response)
    else:
        loader = item_loader(response=response)
    loader.setup()
    if callback:
        callback(loader)
    item = loader.load_item()
    return item
