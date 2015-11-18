import pytest
from thefuck.rules.no_such_file import match, get_new_command
from tests.utils import Command


@pytest.mark.parametrize('command', [
    Command(script='mv foo bar/foo', stderr="mv: cannot move 'foo' to 'bar/foo': No such file or directory"),
    Command(script='mv foo bar/', stderr="mv: cannot move 'foo' to 'bar/': No such file or directory"),
])
def test_match(command):
    assert match(command)


@pytest.mark.parametrize('command', [
    Command(script='mv foo bar/', stderr=""),
    Command(script='mv foo bar/foo', stderr="mv: permission denied"),
])
def test_not_match(command):
    assert not match(command)


@pytest.mark.parametrize('command, new_command', [
    (Command(script='mv foo bar/foo', stderr="mv: cannot move 'foo' to 'bar/foo': No such file or directory"), 'mkdir -p bar && mv foo bar/foo'),
    (Command(script='mv foo bar/', stderr="mv: cannot move 'foo' to 'bar/': No such file or directory"), 'mkdir -p bar && mv foo bar/'),
])
def test_get_new_command(command, new_command):
    assert get_new_command(command) == new_command
