from thefuck.rules.rm_dir import match, get_new_command
from tests.utils import Command


def test_match():
    assert match(Command('rm foo', stderr='rm: foo: is a directory'), None)
    assert match(Command('rm foo', stderr='rm: foo: Is a directory'), None)
    assert not match(Command('rm foo'), None)
    assert not match(Command('rm foo', stderr='foo bar baz'), None)
    assert not match(Command(), None)


def test_get_new_command():
    assert get_new_command(Command('rm foo', '', ''), None) == 'rm -rf foo'
