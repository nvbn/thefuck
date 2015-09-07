import pytest
from thefuck.rules.git_diff_staged import match, get_new_command
from tests.utils import Command


@pytest.mark.parametrize('command', [
    Command(script='git diff foo'),
    Command(script='git diff')])
def test_match(command):
    assert match(command)


@pytest.mark.parametrize('command', [
    Command(script='git diff --staged'),
    Command(script='git tag'),
    Command(script='git branch'),
    Command(script='git log')])
def test_not_match(command):
    assert not match(command)


@pytest.mark.parametrize('command, new_command', [
    (Command('git diff'), 'git diff --staged'),
    (Command('git diff foo'), 'git diff --staged foo')])
def test_get_new_command(command, new_command):
    assert get_new_command(command) == new_command
