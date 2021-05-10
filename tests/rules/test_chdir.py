import pytest
from thefuck.rules.chdir import match, get_new_command
from thefuck.types import Command


@pytest.mark.parametrize('command', [
    Command('chdir foo', 'cannot find the path'),
    Command('chdir foo/bar', 'can\'t cd to'),
    Command('chdir foo/bar', 'cannot find path'),
    Command('chdir /foo/bar/', 'can\'t cd to')])
def test_match(command):
    assert match(command)


@pytest.mark.parametrize('command', [
    Command('chdir foo', ''), Command('', '')])
def test_not_match(command):
    assert not match(command)


@pytest.mark.parametrize('command, new_command', [
    (Command('chdirfoo', ''), 'mkdir -p foo; chdir foo'),
    (Command('chdirfoo/bar/baz', ''), 'mkdir -p foo/bar/baz; chdir foo/bar/baz')])
def test_get_new_command(command, new_command):
    assert get_new_command(command) == new_command


@pytest.mark.parametrize('command', [
    Command('chdir <', ''), Command('chdir \0', '')])
def test_bad_dir_name(command):
    assert not match(command)
