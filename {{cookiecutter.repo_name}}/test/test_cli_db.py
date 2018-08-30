"""Test cases for the databse module of the command-line interface."""
import pytest
from {{ cookiecutter.repo_name }}.cli.db import db
from {{ cookiecutter.repo_name }}.cli.db.mongo import mongo
from {{ cookiecutter.repo_name }}.cli.db.utils import show_db_connectors, show_db_models
from .utils import make_cli_args

EXAMPLE_MONGO_MODEL = 'ExampleMongoModel'


@pytest.mark.mongo
class TestCLIDbMongo:
    """Test cases for `db mongo` module."""

    @pytest.mark.parametrize('arg', [('--show-dbs',), ('--show-models',)])
    def test_db(self, cli_runner, arg):
        """Test cases for DB module."""
        res = cli_runner.invoke(db, [arg])
        assert res.exit_code == 0

    @pytest.mark.parametrize('arg', ['--show-models'])
    def test_mongo(self, cli_runner, arg):
        res = cli_runner.invoke(mongo, [arg])
        assert res.exit_code == 0

    @pytest.mark.parametrize('path_or_name', [EXAMPLE_MONGO_MODEL])
    def test_mongo_schema(self, cli_runner, path_or_name):
        res = cli_runner.invoke(mongo, ['schema', path_or_name])
        assert res.exit_code == 0

    @pytest.mark.parametrize('path_or_name', [EXAMPLE_MONGO_MODEL])
    @pytest.mark.parametrize('query', [
        '{ "number": { "$gt": 75 } }'
    ])
    @pytest.mark.parametrize('field', ['-ftext'])
    @pytest.mark.parametrize('exclude', ['--exclude', ''])
    @pytest.mark.parametrize('limit', ['', '-l10'])
    @pytest.mark.parametrize('skip', ['', '-s20'])
    @pytest.mark.parametrize('order', ['', '-onumber', '-o-number'])
    @pytest.mark.parametrize('dry', ['', '--dry-run'])
    def test_mongo_find(self, cli_runner, path_or_name, query, field, exclude,
                        limit, skip, order, dry):
        args = make_cli_args('find', path_or_name, query, field,
                         exclude, limit, skip, order, dry)
        res = cli_runner.invoke(mongo, args)
        assert res.exit_code == 0

    @pytest.mark.parametrize('path_or_name', [EXAMPLE_MONGO_MODEL])
    @pytest.mark.parametrize('query', [
        '{ "text": { "$in": [ "a112", "a17" ] } }'
    ])
    @pytest.mark.parametrize('dry', ['', '--dry-run'])
    def test_mongo_remove(self, cli_runner, path_or_name, query, dry):
        args = make_cli_args('remove', path_or_name, query, dry)
        res = cli_runner.invoke(mongo, args)
        assert res.exit_code == 0

    @pytest.mark.parametrize('path_or_name', [EXAMPLE_MONGO_MODEL])
    @pytest.mark.parametrize('query,update', [(
        '{ "text": "a112" }',
        '{ "$set": { "number": 112 } }'
    )])
    @pytest.mark.parametrize('upsert,multiple', [('--upsert', '--multiple')])
    @pytest.mark.parametrize('dry', ['', '--dry-run'])
    def test_mongo_update(self, cli_runner, path_or_name, query,
                          update, upsert, multiple, dry):
        args = make_cli_args('update', path_or_name, query,
                         update, upsert, multiple, dry)
        res = cli_runner.invoke(mongo, args)
        assert res.exit_code == 0

    @pytest.mark.parametrize('path_or_name', [EXAMPLE_MONGO_MODEL])
    @pytest.mark.parametrize('pipeline', [(
        '{ "$match": { "number": { "$gt": 100 } } }',
        '{ "$limit": 10 }',
        '{ "$group": { "_id": "$text", "n": { "$sum": "$number" } } }'
    )])
    @pytest.mark.parametrize('dry', ['', '--dry-run'])
    def test_mongo_aggregate(self, cli_runner, path_or_name, pipeline, dry):
        args = make_cli_args('aggregate', path_or_name, *pipeline, dry)
        res = cli_runner.invoke(mongo, args)
        assert res.exit_code == 0

    @pytest.mark.parametrize('path_or_name', [EXAMPLE_MONGO_MODEL])
    @pytest.mark.parametrize('prompt', ['n'])
    def test_mongo_drop(self, cli_runner, path_or_name, prompt):
        args = make_cli_args('drop', path_or_name)
        res = cli_runner.invoke(mongo, args, input=prompt)
        assert res.exit_code == 1
