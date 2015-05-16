from thefuck.rules.grep_recursive import match, get_new_command
from tests.utils import Command


def test_match():
    assert match(Command('grep blah .', stderr='grep: .: Is a directory'), None)
    assert not match(Command(), None)


def test_get_new_command():
    assert get_new_command(
        Command('grep blah .'), None) == 'grep -r blah .'
