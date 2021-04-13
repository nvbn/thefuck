import pytest
from thefuck.rules.cd_mkdir import match, get_new_command
from thefuck.types import Command


@pytest.mark.parametrize('command', [
    Command('chdir foo', 'cannot find the path'),
    Command('chdir foo/bar', 'can\'t cd to'),
    Command('chdir foo/bar', 'cannot find paht'),
    Command('chdir /foo/bar/', 'can\'t cd to')])
def test_match(command):
    assert match(command)


@pytest.mark.parametrize('command', [
    Command('chdir foo', ''), Command('', '')])
def test_not_match(command):
    assert not match(command)


@pytest.mark.parametrize('command, new_command', [
    (Command('chdir foo', ''), 'mkdir -p foo && chdir foo'),
    (Command('chdir foo/bar', ''), 'mkdir -p foo/bar && chdir foo/bar')])
def test_get_new_command(command, new_command):
    assert get_new_command(command) == new_command
