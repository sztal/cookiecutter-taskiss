# """Test cases for the base spider class."""
# import pytest


# @pytest.mark.scrapy
# @pytest.mark.parametrize('limit', [None, 1])
# @pytest.mark.parametrize('mode', ['debug'])
# def test_spidercls(crawler_process, google_spider, limit, mode):
#     """Test case for `BaseSpider`."""
#     data = {}
#     google_spider.data = data
#     google_spider.limit = limit
#     google_spider.mode = mode
#     crawler_process.crawl(google_spider)
#     crawler_process.start()
#     assert data == {}
