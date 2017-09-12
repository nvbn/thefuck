from thefuck.rules.ls_lah import match, get_new_command
from thefuck.types import Command


def test_match():
    assert match(Command('ls', ''))
    assert match(Command('ls file.py', ''))
    assert match(Command('ls /opt', ''))
    assert not match(Command('ls -lah /opt', ''))
    assert not match(Command('pacman -S binutils', ''))
    assert not match(Command('lsof', ''))


def test_get_new_command():
    assert get_new_command(Command('ls file.py', '')) == 'ls -lah file.py'
    assert get_new_command(Command('ls', '')) == 'ls -lah'
