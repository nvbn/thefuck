from thefuck.rules.ls_lah import match, get_new_command
from tests.utils import Command


def test_match():
    assert match(Command(script='ls'))
    assert match(Command(script='ls file.py'))
    assert match(Command(script='ls /opt'))
    assert not match(Command(script='ls -lah /opt'))
    assert not match(Command(script='pacman -S binutils'))
    assert not match(Command(script='lsof'))


def test_get_new_command():
    assert get_new_command(Command(script='ls file.py')) == 'ls -lah file.py'
    assert get_new_command(Command(script='ls')) == 'ls -lah'
