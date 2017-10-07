import pytest
from thefuck.rules.git_remote_delete import get_new_command, match
from thefuck.types import Command


def test_match():
    assert match(Command('git remote delete foo', ''))


@pytest.mark.parametrize('command', [
    Command('git remote remove foo', ''),
    Command('git remote add foo', ''),
    Command('git commit', '')
])
def test_not_match(command):
    assert not match(command)


def test_get_new_command():
    new_command = get_new_command(Command('git remote delete foo', ''))
    assert new_command == 'git remote remove foo'
