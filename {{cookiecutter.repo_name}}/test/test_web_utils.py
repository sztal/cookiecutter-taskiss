"""Test cases for `web.utils` module."""
import pytest
from {{ cookiecutter.repo_name }}.webscraping.utils import get_url_domain, is_url_in_domains
from {{ cookiecutter.repo_name }}.webscraping.utils import normalize_web_content, load_item
from {{ cookiecutter.repo_name }}.webscraping.utils import sectionize, strip, split


@pytest.mark.scrapy
class TestWebscrapingUtils:
    """Test cases for `web.utils` module."""

    @pytest.mark.parametrize('url,exp', [
        ('http://google.com', 'google.com'),
        ('https://doc.scrapy.org/en/latest/', 'scrapy.org')
    ])
    def test_get_url_domain(self, url, exp):
        """Test cases for 'get_url_domain'."""
        res = get_url_domain(url)
        assert res == exp

    @pytest.mark.parametrize('url,domains,exp', [
        ('http://google.com', 'google.com', True),
        ('https://doc.scrapy.org/en/latest/', ['doc.scrapy.org'], False),
        ('www.facebook.com', ['facebook.com', 'example.com'], True)
    ])
    def test_is_url_in_domains(self, url, domains, exp):
        """Test cases for `is_url_in_domains`."""
        res = is_url_in_domains(url, domains)
        assert res == exp

    @pytest.mark.parametrize('x,kwds,exp', [
        ('<strong>Title</strong>', {}, '____SECTION____Title____SECTION____'),
        ('<div><!-- some comment -->and text</div>', {}, 'and text'),
        ('<h1>Title</h1>', {'token': '_TOK_'}, '_TOK_Title_TOK_'),
        ('<div>XXX</div>', {'token': '_DIV_', 'keep': ['div']}, '_DIV_XXX_DIV_'),
        ('<p>Some text</p>', {}, 'Some text')
    ])
    def test_normalize_web_content_simple(self, x, kwds, exp):
        """Test cases for `normalize_web_content`."""
        res = normalize_web_content(x, **kwds)
        assert next(res) == exp

    def test_normalize_web_content_html_markup(self, html_markup):
        """Test case for `normalize_web_content` with actual HTML markup."""
        res = [ x for x in normalize_web_content(html_markup) ]
        exp = [
            "____SECTION____Title____SECTION____",
            "Some text goes here. This is a tremendously interesting article!",
            "Can't stop reading it, oh my!",
            "Even better! Here goes a next paragraph!",
            "What a feast for a hungry reader!",
            "____SECTION____Subtitle____SECTION____",
            "Another story.",
            "This time it is boring as hell.",
            "Better stop reading now.",
            "Some footer"
        ]
        assert res == exp

    def test_load_item(self, html_markup, item_loader):
        """Test case for `load_item` function."""
        res = load_item(html_markup, item_loader)
        exp = item_loader.default_item_class(
            date='2009-01-02',
            title='Title',
            subtitle='Subtitle',
            content=[
                "Some text goes here. This is a tremendously interesting article!",
                "Can't stop reading it, oh my!",
                "Even better! Here goes a next paragraph!",
                "What a feast for a hungry reader!",
                "Another story.",
                "This time it is boring as hell.",
                "Better stop reading now."
            ],
            footer='Some footer'
        )
        assert res == exp

    @pytest.mark.parametrize('parts,first_is_heading,exp', [(
        ['Something', 'Something else', 'And now something completely different'],
        True,
        ['Something\nSomething else', 'And now something completely different']
    ), (
        ['Something', 'Something else', 'And now something completely different'],
        False,
        ['Something', 'Something else\nAnd now something completely different']
    ), (
        ['Something', 'Something else'],
        True,
        ['Something\nSomething else']
    ), (
        ['Something', 'Something else'],
        False,
        ['Something', 'Something else']
    )])
    def test_sectionize(self, parts, first_is_heading, exp):
        """Test cases for `sectionize`."""
        res = sectionize(parts, first_is_heading)
        assert res == exp

    @pytest.mark.parametrize('x,exp', [('a', 'a'), (' a ', 'a'), (3, 3)])
    def test_strip(self, x, exp):
        """Test cases for `strip`."""
        res = strip(x)
        assert res == exp

    @pytest.mark.parametrize('x,divider,exp', [
        ('aa__bb', '__', ['aa', 'bb']),
        ([3, 3], '\n', [3, 3]),
        ('aa', '__', ['aa'])
    ])
    def test_split(self, x, divider, exp):
        """Test cases for `split`."""
        res = split(x, divider)
        assert res == exp
