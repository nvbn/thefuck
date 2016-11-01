from thefuck.rules.ls_all import match, get_new_command
from tests.utils import Command


def test_match():
    assert match(Command(script='ls'))
    assert not match(Command(script='ls', stdout='file.py\n'))


def test_get_new_command():
    assert get_new_command(Command(script='ls empty_dir')) == 'ls -A empty_dir'
    assert get_new_command(Command(script='ls')) == 'ls -A'
