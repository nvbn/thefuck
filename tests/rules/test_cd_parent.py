from thefuck.rules.cd_parent import match, get_new_command
from tests.utils import Command


def test_match():
    assert match(Command('cd..', stderr='cd..: command not found'))
    assert not match(Command())


def test_get_new_command():
    assert get_new_command(
        Command('cd..')) == 'cd ..'
