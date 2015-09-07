from thefuck.rules.man_no_space import match, get_new_command
from tests.utils import Command


def test_match():
    assert match(Command('mandiff', stderr='mandiff: command not found'))
    assert not match(Command())


def test_get_new_command():
    assert get_new_command(
        Command('mandiff')) == 'man diff'
