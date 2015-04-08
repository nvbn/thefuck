from thefuck.main import Command
from thefuck.rules.sudo import match, get_new_command


def test_match():
    assert match(Command('', '', 'Permission denied'))
    assert match(Command('', '', 'permission denied'))
    assert not match(Command('', '', ''))


def test_get_new_command():
    assert get_new_command(Command('ls', '', '')) == 'sudo ls'
