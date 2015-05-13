import pytest
from thefuck import shells


@pytest.fixture
def builtins_open(mocker):
    return mocker.patch('six.moves.builtins.open')


@pytest.fixture
def isfile(mocker):
    return mocker.patch('os.path.isfile', return_value=True)


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
    def Popen(self, mocker):
        mock = mocker.patch('thefuck.shells.Popen')
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
        builtins_open.return_value.__enter__.return_value. \
            write.assert_called_once_with('ls\n')


@pytest.mark.usefixtures('isfile')
class TestZsh(object):
    @pytest.fixture(autouse=True)
    def Popen(self, mocker):
        mock = mocker.patch('thefuck.shells.Popen')
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

    def test_put_to_history(self, builtins_open, mocker):
        mocker.patch('thefuck.shells.time',
                     return_value=1430707243.3517463)
        shells.Zsh().put_to_history('ls')
        builtins_open.return_value.__enter__.return_value. \
            write.assert_called_once_with(': 1430707243:0;ls\n')
