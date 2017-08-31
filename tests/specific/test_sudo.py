import pytest
from thefuck.specific.sudo import sudo_support
from thefuck.types import Command


@pytest.mark.parametrize('return_value, command, called, result', [
    ('ls -lah', 'sudo ls', 'ls', 'sudo ls -lah'),
    ('ls -lah', 'ls', 'ls', 'ls -lah'),
    (['ls -lah'], 'sudo ls', 'ls', ['sudo ls -lah']),
    (True, 'sudo ls', 'ls', True),
    (True, 'ls', 'ls', True),
    (False, 'sudo ls', 'ls', False),
    (False, 'ls', 'ls', False)])
def test_sudo_support(return_value, command, called, result):
    def fn(command):
        assert command == Command(called, '')
        return return_value

    assert sudo_support(fn)(Command(command, '')) == result
