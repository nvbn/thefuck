import pytest
from mock import Mock, MagicMock
from thefuck import shells


@pytest.fixture
def builtins_open(monkeypatch):
    mock = MagicMock()
    monkeypatch.setattr('six.moves.builtins.open', mock)
    return mock


@pytest.fixture
def isfile(monkeypatch):
    mock = Mock(return_value=True)
    monkeypatch.setattr('os.path.isfile', mock)
    return mock


class TestGeneric(object):
    def test_from_shell(self):
        assert shells.Generic().from_shell('pwd') == 'pwd'

    def test_to_shell(self):
        assert shells.Generic().to_shell('pwd') == 'pwd'

    def test_put_to_history(self, builtins_open):
        assert shells.Generic().put_to_history('ls') is None
        assert builtins_open.call_count == 0


@pytest.mark.usefixtures('isfile')
class TestBash(object):
    @pytest.fixture(autouse=True)
    def Popen(self, monkeypatch):
        mock = Mock()
        monkeypatch.setattr('thefuck.shells.Popen', mock)
        mock.return_value.stdout.read.return_value = (
            b'alias l=\'ls -CF\'\n'
            b'alias la=\'ls -A\'\n'
            b'alias ll=\'ls -alF\'')
        return mock

    @pytest.mark.parametrize('before, after', [
        ('pwd', 'pwd'),
        ('ll', 'ls -alF')])
    def test_from_shell(self, before, after):
        assert shells.Bash().from_shell(before) == after

    def test_to_shell(self):
        assert shells.Bash().to_shell('pwd') == 'pwd'

    def test_put_to_history(self, builtins_open):
        shells.Bash().put_to_history('ls')
        builtins_open.return_value.__enter__.return_value.\
            write.assert_called_once_with('ls\n')


@pytest.mark.usefixtures('isfile')
class TestZsh(object):
    @pytest.fixture(autouse=True)
    def Popen(self, monkeypatch):
        mock = Mock()
        monkeypatch.setattr('thefuck.shells.Popen', mock)
        mock.return_value.stdout.read.return_value = (
            b'l=\'ls -CF\'\n'
            b'la=\'ls -A\'\n'
            b'll=\'ls -alF\'')
        return mock

    @pytest.mark.parametrize('before, after', [
        ('pwd', 'pwd'),
        ('ll', 'ls -alF')])
    def test_from_shell(self, before, after):
        assert shells.Zsh().from_shell(before) == after

    def test_to_shell(self):
        assert shells.Zsh().to_shell('pwd') == 'pwd'

    def test_put_to_history(self, builtins_open, monkeypatch):
        monkeypatch.setattr('thefuck.shells.time',
                            lambda: 1430707243.3517463)
        shells.Zsh().put_to_history('ls')
        builtins_open.return_value.__enter__.return_value. \
            write.assert_called_once_with(': 1430707243:0;ls\n')