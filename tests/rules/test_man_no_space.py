from thefuck.rules.man_no_space import get_new_command, match
from thefuck.types import Command


def test_match():
    assert match(Command('mandiff', 'mandiff: command not found'))
    assert not match(Command('', ''))


def test_get_new_command():
    assert get_new_command(Command('mandiff', '')) == 'man diff'
