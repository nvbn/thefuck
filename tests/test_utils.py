from mock import Mock
from thefuck.utils import sudo_support
from thefuck.main import Command


def test_sudo_support():
    fn = Mock(return_value=True, __name__='')
    assert sudo_support(fn)(Command('sudo ls', 'out', 'err'), None)
    fn.assert_called_once_with(Command('ls', 'out', 'err'), None)

    fn.return_value = False
    assert not sudo_support(fn)(Command('sudo ls', 'out', 'err'), None)

    fn.return_value = 'pwd'
    assert sudo_support(fn)(Command('sudo ls', 'out', 'err'), None) == 'sudo pwd'

    assert sudo_support(fn)(Command('ls', 'out', 'err'), None) == 'pwd'
