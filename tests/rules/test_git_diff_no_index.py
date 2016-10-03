import pytest
from thefuck.rules.git_diff_no_index import match, get_new_command
from tests.utils import Command


@pytest.mark.parametrize('command', [
    Command(script='git diff foo bar')])
def test_match(command):
    assert match(command)


@pytest.mark.parametrize('command', [
    Command(script='git diff --no-index foo bar'),
    Command(script='git diff foo'),
    Command(script='git diff foo bar baz')])
def test_not_match(command):
    assert not match(command)


@pytest.mark.parametrize('command, new_command', [
    (Command('git diff foo bar'), 'git diff --no-index foo bar')])
def test_get_new_command(command, new_command):
    assert get_new_command(command) == new_command
