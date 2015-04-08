from thefuck.main import Command
from thefuck.rules.sudo import match, get_new_command


def test_match():
    assert match(Command('', '', 'Permission denied'), None)
    assert match(Command('', '', 'permission denied'), None)
    assert match(Command('', '', "npm ERR! Error: EACCES, unlink"), None)
    assert not match(Command('', '', ''), None)


def test_get_new_command():
    assert get_new_command(Command('ls', '', ''), None) == 'sudo ls'
