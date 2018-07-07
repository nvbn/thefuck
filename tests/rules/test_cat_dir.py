import pytest
from thefuck.rules.cat_dir import match, get_new_command
from thefuck.types import Command


@pytest.mark.parametrize('command', [
    Command('cat foo', 'cat: foo: Is a directory'),
    Command('cat /foo/bar/', 'cat: /foo/bar/: Is a directory'),
])
def test_match(command):
    assert match(command)


@pytest.mark.parametrize('command', [
    Command('cat foo', 'foo bar baz'),
    Command('cat foo bar', 'foo bar baz'),
    Command('', ''),
])
def test_not_match(command):
    assert not match(command)


@pytest.mark.parametrize('command, new_command', [
    (Command('cat foo', 'cat: foo: Is a directory'), 'ls foo'),
    (Command('cat /foo/bar/', 'cat: /foo/bar/: Is a directory'), 'ls /foo/bar/'),
])
def test_get_new_command(command, new_command):
    assert get_new_command(command) == new_command
