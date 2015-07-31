import pytest
from thefuck.rules.brew_unknown_command import match, get_new_command
from thefuck.rules.brew_unknown_command import brew_commands
from tests.utils import Command


@pytest.fixture
def brew_unknown_cmd():
    return '''Error: Unknown command: inst'''


@pytest.fixture
def brew_unknown_cmd2():
    return '''Error: Unknown command: instaa'''


def test_match(brew_unknown_cmd):
    assert match(Command('brew inst', stderr=brew_unknown_cmd), None)
    for command in brew_commands:
        assert not match(Command('brew ' + command), None)


def test_get_new_command(brew_unknown_cmd, brew_unknown_cmd2):
    assert get_new_command(Command('brew inst', stderr=brew_unknown_cmd),
                           None) == ['brew list', 'brew install', 'brew uninstall']

    assert get_new_command(Command('brew instaa', stderr=brew_unknown_cmd2),
                           None) == ['brew install', 'brew uninstall', 'brew list']
