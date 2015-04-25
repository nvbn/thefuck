from thefuck.rules.sudo import match, get_new_command
from tests.utils import Command


def test_match():
    assert match(Command(stderr='Permission denied'), None)
    assert match(Command(stderr='permission denied'), None)
    assert match(Command(stderr="npm ERR! Error: EACCES, unlink"), None)
    assert not match(Command(), None)


def test_get_new_command():
    assert get_new_command(Command('ls'), None) == 'sudo ls'
