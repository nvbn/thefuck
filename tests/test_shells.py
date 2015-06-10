import pytest
from thefuck import shells


@pytest.fixture
def builtins_open(mocker):
    return mocker.patch('six.moves.builtins.open')


@pytest.fixture
def isfile(mocker):
    return mocker.patch('os.path.isfile', return_value=True)


class TestGeneric(object):
    @pytest.fixture
    def shell(self):
        return shells.Generic()

    def test_from_shell(self, shell):
        assert shell.from_shell('pwd') == 'pwd'

    def test_to_shell(self, shell):
        assert shell.to_shell('pwd') == 'pwd'

    def test_put_to_history(self, builtins_open, shell):
        assert shell.put_to_history('ls') is None
        assert builtins_open.call_count == 0

    def test_and_(self, shell):
        assert shell.and_('ls', 'cd') == 'ls && cd'

    def test_get_aliases(self, shell):
        assert shell.get_aliases() == {}


@pytest.mark.usefixtures('isfile')
class TestBash(object):
    @pytest.fixture
    def shell(self):
        return shells.Bash()

    @pytest.fixture(autouse=True)
    def Popen(self, mocker):
        mock = mocker.patch('thefuck.shells.Popen')
        mock.return_value.stdout.read.return_value = (
            b'alias fuck=\'eval $(thefuck $(fc -ln -1))\'\n'
            b'alias l=\'ls -CF\'\n'
            b'alias la=\'ls -A\'\n'
            b'alias ll=\'ls -alF\'')
        return mock

    @pytest.mark.parametrize('before, after', [
        ('pwd', 'pwd'),
        ('fuck', 'eval $(thefuck $(fc -ln -1))'),
        ('awk', 'awk'),
        ('ll', 'ls -alF')])
    def test_from_shell(self, before, after, shell):
        assert shell.from_shell(before) == after

    def test_to_shell(self, shell):
        assert shell.to_shell('pwd') == 'pwd'

    def test_put_to_history(self, builtins_open, shell):
        shell.put_to_history('ls')
        builtins_open.return_value.__enter__.return_value. \
            write.assert_called_once_with('ls\n')

    def test_and_(self, shell):
        assert shell.and_('ls', 'cd') == 'ls && cd'

    def test_get_aliases(self, shell):
        assert shell.get_aliases() == {'fuck': 'eval $(thefuck $(fc -ln -1))',
                                       'l': 'ls -CF',
                                       'la': 'ls -A',
                                       'll': 'ls -alF'}


@pytest.mark.usefixtures('isfile')
class TestFish(object):
    @pytest.fixture
    def shell(self):
        return shells.Fish()

    @pytest.fixture(autouse=True)
    def Popen(self, mocker):
        mock = mocker.patch('thefuck.shells.Popen')
        mock.return_value.stdout.read.return_value = (
            b'fish_config\nfuck\nfunced\nfuncsave\ngrep\nhistory\nll\nmath')
        return mock

    @pytest.mark.parametrize('before, after', [
        ('pwd', 'pwd'),
        ('fuck', 'fish -ic "fuck"'),
        ('find', 'find'),
        ('funced', 'fish -ic "funced"'),
        ('awk', 'awk'),
        ('math "2 + 2"', r'fish -ic "math \"2 + 2\""'),
        ('vim', 'vim'),
        ('ll', 'fish -ic "ll"')])  # Fish has no aliases but functions
    def test_from_shell(self, before, after, shell):
        assert shell.from_shell(before) == after

    def test_to_shell(self, shell):
        assert shell.to_shell('pwd') == 'pwd'

    def test_put_to_history(self, builtins_open, mocker, shell):
        mocker.patch('thefuck.shells.time',
                     return_value=1430707243.3517463)
        shell.put_to_history('ls')
        builtins_open.return_value.__enter__.return_value. \
            write.assert_called_once_with('- cmd: ls\n   when: 1430707243\n')

    def test_and_(self, shell):
        assert shell.and_('foo', 'bar') == 'foo; and bar'

    def test_get_aliases(self, shell):
        assert shell.get_aliases() == {'fish_config': 'fish_config',
                                       'fuck': 'fuck',
                                       'funced': 'funced',
                                       'funcsave': 'funcsave',
                                       'grep': 'grep',
                                       'history': 'history',
                                       'll': 'll',
                                       'math': 'math'}


@pytest.mark.usefixtures('isfile')
class TestZsh(object):
    @pytest.fixture
    def shell(self):
        return shells.Zsh()

    @pytest.fixture(autouse=True)
    def Popen(self, mocker):
        mock = mocker.patch('thefuck.shells.Popen')
        mock.return_value.stdout.read.return_value = (
            b'fuck=\'eval $(thefuck $(fc -ln -1 | tail -n 1))\'\n'
            b'l=\'ls -CF\'\n'
            b'la=\'ls -A\'\n'
            b'll=\'ls -alF\'')
        return mock

    @pytest.mark.parametrize('before, after', [
        ('fuck', 'eval $(thefuck $(fc -ln -1 | tail -n 1))'),
        ('pwd', 'pwd'),
        ('ll', 'ls -alF')])
    def test_from_shell(self, before, after, shell):
        assert shell.from_shell(before) == after

    def test_to_shell(self, shell):
        assert shell.to_shell('pwd') == 'pwd'

    def test_put_to_history(self, builtins_open, mocker, shell):
        mocker.patch('thefuck.shells.time',
                     return_value=1430707243.3517463)
        shell.put_to_history('ls')
        builtins_open.return_value.__enter__.return_value. \
            write.assert_called_once_with(': 1430707243:0;ls\n')

    def test_and_(self, shell):
        assert shell.and_('ls', 'cd') == 'ls && cd'

    def test_get_aliases(self, shell):
        assert shell.get_aliases() == {
            'fuck': 'eval $(thefuck $(fc -ln -1 | tail -n 1))',
            'l': 'ls -CF',
            'la': 'ls -A',
            'll': 'ls -alF'}
