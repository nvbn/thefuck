from thefuck.rules.man_no_space import match, get_new_command
from tests.utils import Command


def test_match():
    assert match(Command('mandiff', stderr='mandiff: command not found'), None)
    assert not match(Command(), None)


def test_get_new_command():
    assert get_new_command(
        Command('mandiff'), None) == 'man diff'
