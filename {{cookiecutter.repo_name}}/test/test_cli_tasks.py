"""Test cases for the `tasks` module of the command-line interface."""
import pytest
from {{ cookiecutter.repo_name }}.cli.tasks import tasks
from .utils import make_cli_args


@pytest.mark.task
class TestCLITasks:
    """Test cases for `db tasks` module."""

    # @pytest.mark.parametrize('command', [
    #     'stats',
    #     'report',
    #     'ping',
    #     'active-queues',
    #     'registered',
    #     'active',
    #     'scheduled',
    #     'reserved',
    #     'revoked',
    #     'conf'
    # ])
    # def test_basic_commands(self, cli_runner, command):
    #     args = make_cli_args(command)
    #     res = cli_runner.invoke(tasks, args)
    #     assert res.exit_code == 0

    @pytest.mark.parametrize('task,arg,parg', [
        ('t5', ('-a x=10', '-a y=20'), ()),
        ('cfg', (), ('-p cfg={ "a": 1, "b": 2 }',))
    ])
    @pytest.mark.parametrize('get', ['', '-g2'])
    @pytest.mark.parametrize('argparser', [
        '-Pjson',
        '-Peval'
    ])
    @pytest.mark.parametrize('dry', ['', '--dry-run'])
    def test_run(self, cli_runner, task, arg, parg, get, argparser, dry):
        args = make_cli_args('run', task, *arg, *parg, get, argparser)
        res = cli_runner.invoke(tasks, args)
        assert res.exit_code == 0
