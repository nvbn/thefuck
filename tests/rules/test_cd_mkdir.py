import pytest
from thefuck.rules.cd_mkdir import match, get_new_command
from tests.utils import Command


@pytest.mark.parametrize('command', [
    Command(script='cd foo', stderr='cd: foo: No such file or directory'),
    Command(script='cd foo/bar/baz',
            stderr='cd: foo: No such file or directory'),
    Command(script='cd foo/bar/baz', stderr='cd: can\'t cd to foo/bar/baz')])
def test_match(command):
    assert match(command)


@pytest.mark.parametrize('command', [
    Command(script='cd foo', stderr=''), Command()])
def test_not_match(command):
    assert not match(command)


@pytest.mark.parametrize('command, new_command', [
    (Command('cd foo'), 'mkdir -p foo && cd foo'),
    (Command('cd foo/bar/baz'), 'mkdir -p foo/bar/baz && cd foo/bar/baz')])
def test_get_new_command(command, new_command):
    assert get_new_command(command) == new_command
