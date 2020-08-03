import pytest
from thefuck.rules.version import match, get_new_command
from thefuck.types import Command


@pytest.mark.parametrize('command', [
    Command('git -v', ''),
    Command('git -version', ''),
    Command('git -version', ''),
    Command('fuck -ver', '')])
def test_match(command):
    assert match(command)


@pytest.mark.parametrize('command, new_command', [
    (Command('git -v', ''), 'git --version'),
    (Command('git -version', ''), 'git --version'),
    (Command('fuck -ver', ''), 'fuck --version')])
def test_get_new_command(command, new_command):
    assert get_new_command(command) == new_command
