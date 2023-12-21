import pytest
from thefuck.rules.brew_unknown_command import match, get_new_command
from thefuck.rules.brew_unknown_command import _brew_commands
from thefuck.types import Command


@pytest.fixture
def brew_unknown_cmd():
    return '''Error: Unknown command: inst'''


@pytest.fixture
def brew_unknown_cmd2():
    return '''Error: Unknown command: instaa'''


@pytest.fixture
def brew_unknown_cmd_auto():
    return '''Error: Unknown command: auto'''


@pytest.fixture
def brew_unknown_cmd_outdated():
    return '''Error: Unknown command: outdate'''


def test_match(brew_unknown_cmd):
    assert match(Command('brew inst', brew_unknown_cmd))
    for command in _brew_commands():
        assert not match(Command('brew ' + command, ''))


def test_get_new_command(brew_unknown_cmd, brew_unknown_cmd2, brew_unknown_cmd_auto,
                         brew_unknown_cmd_outdated):
    assert (get_new_command(Command('brew inst', brew_unknown_cmd))
            == ['brew list', 'brew install', 'brew uninstall'])

    cmds = get_new_command(Command('brew instaa', brew_unknown_cmd2))
    assert 'brew install' in cmds
    assert 'brew uninstall' in cmds

    cmds = get_new_command(Command('brew auto', brew_unknown_cmd_auto))
    assert 'brew audit' in cmds
    assert 'brew autoremove' in cmds

    cmds = get_new_command(Command('brew outdate', brew_unknown_cmd_outdated))
    assert 'brew outdated' in cmds
    assert 'brew update' in cmds
    assert 'brew bottle' in cmds
