import pytest
from subprocess import PIPE
from mock import Mock
from thefuck import main
from tests.utils import Command


class TestGetCommand(object):
    @pytest.fixture(autouse=True)
    def Popen(self, monkeypatch):
        Popen = Mock()
        Popen.return_value.stdout.read.return_value = b'stdout'
        Popen.return_value.stderr.read.return_value = b'stderr'
        monkeypatch.setattr('thefuck.main.Popen', Popen)
        return Popen

    @pytest.fixture(autouse=True)
    def prepare(self, monkeypatch):
        monkeypatch.setattr('thefuck.main.os.environ', {})
        monkeypatch.setattr('thefuck.main.wait_output', lambda *_: True)

    @pytest.fixture(autouse=True)
    def generic_shell(self, monkeypatch):
        monkeypatch.setattr('thefuck.shells.from_shell', lambda x: x)
        monkeypatch.setattr('thefuck.shells.to_shell', lambda x: x)

    def test_get_command_calls(self, Popen, settings):
        settings.env = {}
        assert main.get_command(['thefuck', 'apt-get', 'search', 'vim']) \
               == Command('apt-get search vim', 'stdout', 'stderr')
        Popen.assert_called_once_with('apt-get search vim',
                                      shell=True,
                                      stdout=PIPE,
                                      stderr=PIPE,
                                      env={})

    @pytest.mark.parametrize('args, result', [
        (['thefuck', ''], None),
        (['thefuck', '', ''], None),
        (['thefuck', 'ls', '-la'], 'ls -la'),
        (['thefuck', 'ls'], 'ls')])
    def test_get_command_script(self, args, result):
        if result:
            assert main.get_command(args).script == result
        else:
            assert main.get_command(args) is None
