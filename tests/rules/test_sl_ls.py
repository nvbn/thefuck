
from thefuck.rules.sl_ls import get_new_command, match
from thefuck.types import Command


def test_match():
    assert match(Command('sl', ''))
    assert not match(Command('ls', ''))


def test_get_new_command():
    assert get_new_command(Command('sl', '')) == 'ls'
