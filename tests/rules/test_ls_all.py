from thefuck.rules.ls_all import match, get_new_command
from thefuck.types import Command


def test_match():
    assert match(Command('ls', ''))
    assert not match(Command('ls', 'file.py\n'))


def test_get_new_command():
    assert get_new_command(Command('ls empty_dir', '')) == 'ls -A empty_dir'
    assert get_new_command(Command('ls', '')) == 'ls -A'
