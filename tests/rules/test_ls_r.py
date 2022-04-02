from thefuck.rules.sl_ls import match, get_new_command
from thefuck.types import Command


def test_match():
    assert match(Command('ls -r', ''))
    assert not match(Command('ls -R', ''))


def test_get_new_command():
    assert get_new_command(Command('ls -r', '')) == 'ls -R'
