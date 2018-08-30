"""Shared configuration and fixtures of the test suite.

In principle tasks are tested in two different ways.
Their main logic (defined in `.run()`) method can be in most cases
tested in idempotent and isolated unit tests, although sometimes
it may be necessary to use mocking and/or patching.

Tests can also be run within working
"""
import os
import pytest
from click.testing import CliRunner
from scrapy import Item, Field
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from scrapy.loader.processors import MapCompose
from {{ cookiecutter.repo_name }} import taskiss
from {{ cookiecutter.repo_name }}.config import cfg, MODE
from {{ cookiecutter.repo_name }}.taskiss.scheduler import Scheduler
from {{ cookiecutter.repo_name }}.config.taskiss import include
from {{ cookiecutter.repo_name }}.webscraping.itemcls import BaseItemLoader
from {{ cookiecutter.repo_name }}.webscraping.spidercls import BaseSpider
# Import tasks only if taskiss object is defined
if taskiss:
        import {{ cookiecutter.repo_name }}.tasks as _tasks

# Custom options --------------------------------------------------------------

def pytest_addoption(parser):
    """Additional custom `pytest` command line options."""
    parser.addoption(
        '--all', action='store_true', default=False,
        help="Run all tests. Database test still need to be enabled in the configuration."
    )
    parser.addoption(
        '--run-tasks', action='store_true', default=False,
        help="Run task tests."
    )
    parser.addoption(
        '--run-mongo', action='store_true', default=True,
        help="Run tests dependent on MongoDB."
    )

def pytest_collection_modifyitems(config, items):
    """Modify test runner behavior based on `pytest` settings."""
    use_mongo = cfg.getenvvar(MODE, 'use_mongo', fallback=True, convert_bool=True)
    use_celery = cfg.getenvvar(MODE, 'use_celery', fallback=True, convert_bool=True)
    run_all = config.getoption('--all')
    run_tasks = use_celery and (config.getoption('--run-tasks') or run_all)
    run_mongo = use_mongo and (config.getoption('--run-mongo') or run_all)
    if not run_tasks:
        skip_tasks = pytest.mark.skip(
            reason="need --run-tasks to run and 'USE_CELERY' enabled to run."
        )
        for item in items:
            if "task" in item.keywords:
                item.add_marker(skip_tasks)
    if not run_mongo:
        skip_db_tasks = pytest.mark.skip(
            reason="need --run-mongo and envvar 'USE_MONGO' enabled to run."
        )
        for item in items:
            if "mongo" in item.keywords:
                item.add_marker(skip_db_tasks)

# Fixtures --------------------------------------------------------------------

@pytest.fixture(scope='session')
def taskiss():
    """Fixture: *Taskiss* application object."""
    if taskiss:
        taskiss.scheduler.get_registered_tasks()
        taskiss.scheduler.build_dependency_graph()
    return taskiss

@pytest.fixture(scope='session')
def tasks():
    """Fixture: *Taskiss* tasks."""
    return _tasks

@pytest.fixture(scope='session')
def celery_config():
    """Fixture: basic *Celery* config."""
    return {
        'broker_url':
            os.environ.get('CELERY_TEST_BROKER_URL', 'pyamqp://'),
        'result_backend':
            os.environ.get('CELERY_TEST_RESULT_BACKEND', 'redis://127.0.0.1'),
        'include': ['{{cookiecutter.repo_name}}.tasks'],
        'task_serializer': 'json',
        'result_serializer': 'json',
        'accept_content': ['json'],
        'enable_utc': True
    }

@pytest.fixture(scope='session')
def scheduler():
    """Fixture: *Taskiss* scheduler object."""
    scheduler = Scheduler(include)
    scheduler.get_registered_tasks()
    scheduler.build_dependency_graph()
    return scheduler

@pytest.fixture(scope='session')
def mod_predicate():
    """Fixture: module predicate for handling test when some app parts are disabled."""
    def _mod_predicate(finder, name, ispkg):
        """Module predicate function."""
        celery = cfg.getenvvar(MODE, 'use_celery', fallback=True, convert_bool=True)
        mongo = cfg.getenvvar(MODE, 'use_mongo', fallback=True, convert_bool=True)
        if not celery:
            for dep in include:
                if name.startswith(dep):
                    return False
        mongo_path = '{{ cookiecutter.repo_name }}.persistence.db.mongo'
        if not mongo and name.startswith(mongo_path):
            return False
        return True
    return _mod_predicate

@pytest.fixture
def cli_runner():
    """Command-line test runner."""
    return CliRunner()

# Fixtures for webscrapign testing --------------------------------------------

@pytest.fixture(scope='session')
def html_markup():
    """Fixture: some HTML markup."""
    return """
    <html>
    <head>
        <meta name="date" content="2009-01-02" scheme="YYYY-MM-DD">
    </head>
    <body>
        <div>
            <!-- some comment -->
            <h1>Title</h1>
            <section>
                <div class="wrap">
                    <p>
                        Some text goes here. This is a tremendously interesting article!
                        Can't stop reading it, oh my!
                    </p>
                    <p>
                        Even better! Here goes a next paragraph!
                        What a feast for a hungry reader!
                    </p>
                    <h2>Subtitle</h2>
                    <p>
                        Another story.
                        This time it is boring as hell.
                        Better stop reading now.
                    </p>
                </div>
            </section>
            <footer>
                <span>Some footer</span>
            </footer>
        </div>
    </body>
    </html>
    """

@pytest.fixture(scope='session')
def item_loader():
    """Fixture: test item loader class."""
    class TestItem(Item):
        """Test item class."""
        date = Field()
        title = Field()
        subtitle = Field()
        content = Field()
        footer = Field()

    class TestItemLoader(BaseItemLoader):
        """Test item loader class."""
        default_item_class = TestItem

        container_sel = ('body > div', 'css')
        date_sel = ('/html/head/meta/@content', 'xpath')
        title_sel = ('h1::text', 'css')
        subtitle_sel = ('h2::text', 'css')
        content_sel = ('div.wrap > p::text', 'css')
        footer_sel = ('footer > span::text', 'css')

        content_out = MapCompose()

    return TestItemLoader

@pytest.fixture(scope='session')
def crawler_process():
    """Fixture: *Scrapy* crawler process."""
    crawler_process = CrawlerProcess(get_project_settings())
    return crawler_process

@pytest.fixture(scope='session')
def google_spider():
    """Fixture: test spider extracting content from the main page of *Google*."""
    class GoogleItem(Item):
        """Google item class."""
        name = Field()

    class GoogleItemLoader(BaseItemLoader):
        """Google item loader class."""
        default_item_class = GoogleItem
        container_sel = ('div#main', 'css')
        name_sel = ('center > div > img::attr(alt)', 'css')

    class GoogleSpider(BaseSpider):
        """Google spider."""
        name = 'google'
        start_urls = ['www.google.com']
        allowed_domains = ['google.com']
        data = []

        def parse(self, response):
            """Parse method."""
            item = super().parse(responses)
            self.data.append(item)
            return item

    return GoogleSpider
