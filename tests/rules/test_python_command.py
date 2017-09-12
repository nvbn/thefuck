from thefuck.rules.python_command import match, get_new_command
from thefuck.types import Command


def test_match():
    assert match(Command('temp.py', 'Permission denied'))
    assert not match(Command('', ''))


def test_get_new_command():
    assert (get_new_command(Command('./test_sudo.py', ''))
            == 'python ./test_sudo.py')
