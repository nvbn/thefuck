from thefuck.rules.ls_lah import match, get_new_command
from tests.utils import Command


def test_match():
    assert match(Command(script='ls'), None)
    assert match(Command(script='ls file.py'), None)
    assert match(Command(script='ls /opt'), None)
    assert not match(Command(script='ls -lah /opt'), None)
    assert not match(Command(script='pacman -S binutils'), None)
    assert not match(Command(script='lsof'), None)


def test_get_new_command():
    assert get_new_command(Command(script='ls file.py'), None) == 'ls -lah file.py'
    assert get_new_command(Command(script='ls'), None) == 'ls -lah'
