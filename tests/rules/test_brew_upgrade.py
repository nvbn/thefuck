import pytest
from thefuck.rules.brew_upgrade import match, get_new_command
from thefuck.types import Command


@pytest.mark.parametrize('command', [
    Command('brew upgrade', '')])
def test_match(command):
    assert match(command)


@pytest.mark.parametrize('command, new_command', [
    (Command('brew upgrade', ''), 'brew upgrade --all')])
def test_get_new_command(command, new_command):
    assert get_new_command(command) == new_command
