
from thefuck.types import Command
from thefuck.rules.sl_ls import match, get_new_command


def test_match():
    assert match(Command('sl', '', ''), None)
    assert not match(Command('ls', '', ''), None)


def test_get_new_command():
    assert get_new_command(Command('sl', '', ''), None) == 'ls'
