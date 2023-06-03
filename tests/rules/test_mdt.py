import pytest
from thefuck.rules.mdt import match, get_new_command
from thefuck.types import Command

def test_match():
    assert match(Command('mdt hlp', 'Unknown command\ntry \'mdt help\''))


@pytest.mark.parametrize('command, new_command', [
    (Command('mdt shll', ''), 'mdt shell'),
    (Command('mdt hlp', ''), 'mdt help')
])

def test_get_new_command(command, new_command):
    assert get_new_command(command) == new_command
