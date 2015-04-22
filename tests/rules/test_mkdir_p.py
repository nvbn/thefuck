from thefuck.types import Command
from thefuck.rules.mkdir_p import match, get_new_command


def test_match():
    assert match(Command('mkdir foo/bar/baz', '', 'mkdir: foo/bar: No such file or directory'), None)
    assert not match(Command('mkdir foo/bar/baz', '', ''), None)
    assert not match(Command('mkdir foo/bar/baz', '', 'foo bar baz'), None)
    assert not match(Command('', '', ''), None)


def test_get_new_command():
    assert get_new_command(Command('mkdir foo/bar/baz', '', ''), None) == 'mkdir -p foo/bar/baz'
