from thefuck.main import Command
from thefuck.rules.rm_dir import match, get_new_command


def test_match():
    assert match(Command('rm foo', '', 'rm: foo: is a directory'), None)
    assert match(Command('rm foo', '', 'rm: foo: Is a directory'), None)
    assert not match(Command('rm foo', '', ''), None)
    assert not match(Command('rm foo', '', 'foo bar baz'), None)
    assert not match(Command('', '', ''), None)


def test_get_new_command():
    assert get_new_command(Command('rm foo', '', ''), None) == 'rm -rf foo'
