import pytest
from mock import Mock
from thefuck.specific.sudo import sudo_support
from tests.utils import Command


@pytest.mark.parametrize('return_value, command, called, result', [
    ('ls -lah', 'sudo ls', 'ls', 'sudo ls -lah'),
    ('ls -lah', 'ls', 'ls', 'ls -lah'),
    (['ls -lah'], 'sudo ls', 'ls', ['sudo ls -lah']),
    (True, 'sudo ls', 'ls', True),
    (True, 'ls', 'ls', True),
    (False, 'sudo ls', 'ls', False),
    (False, 'ls', 'ls', False)])
def test_sudo_support(return_value, command, called, result):
    fn = Mock(return_value=return_value, __name__='')
    assert sudo_support(fn)(Command(command), None) == result
    fn.assert_called_once_with(Command(called), None)
