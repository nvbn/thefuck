import pytest
from thefuck.rules.remove_shell_prompt_literal import match, get_new_command
from thefuck.types import Command


@pytest.mark.parametrize('command',
    [
        Command('$ cd newdir', '$: command not found'),
        Command(' $ cd newdir', '$: command not found'),
    ])
def test_match(command):
    assert match(command)


@pytest.mark.parametrize('command',
    [
        Command('$', ''),
        Command('$?', ''),
        Command(' $?', ''),
        Command('', ''),
    ])
def test_not_match(command):
    assert not match(command)


@pytest.mark.parametrize('command, new_command',
    [
        (Command('$ cd newdir', ''), 'cd newdir'),
        (Command('$ python3 -m virtualenv env', ''), 'python3 -m virtualenv env'),
    ])
def test_get_new_command(command, new_command):
    assert get_new_command(command) == new_command
