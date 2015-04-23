import pytest
from thefuck.types import Command
from thefuck.rules.brew_unknown_command import match, get_new_command
from thefuck.rules.brew_unknown_command import brew_commands


@pytest.fixture
def brew_unknown_cmd():
    return '''Error: Unknown command: inst'''


@pytest.fixture
def brew_unknown_cmd_instaa():
    return '''Error: Unknown command: instaa'''


def test_match(brew_unknown_cmd):
    assert match(Command('brew inst', '', brew_unknown_cmd), None)
    for command in brew_commands:
        assert not match(Command('brew ' + command, '', ''), None)


def test_get_new_command(brew_unknown_cmd, brew_unknown_cmd_instaa):
    assert get_new_command(Command('brew inst', '', brew_unknown_cmd), None)\
        == 'brew list'

    assert get_new_command(Command('brew instaa', '', brew_unknown_cmd_instaa),
                           None) == 'brew install'
