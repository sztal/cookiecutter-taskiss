# """Test cases for the base spider class."""
import pytest


@pytest.mark.scrapy
def test_spidercls(crawler_process, wikipedia_spider):
    """Test case for `BaseSpider`."""
    data = []
    limit = 10
    wikipedia_spider.data = data
    wikipedia_spider.limit = limit
    crawler_process.crawl(wikipedia_spider)
    crawler_process.start()
    wikipedia_spider.args.limit = limit
    assert data == [{ 'name': 'Wikipedia' }]
