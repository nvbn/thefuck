import pytest

from thefuck.rules.smart_command_suggestion import match, get_new_command
from thefuck.types import Command


@pytest.fixture(autouse=True)
def executables(mocker):
    return mocker.patch(
        'thefuck.rules.smart_command_suggestion.get_all_executables',
        return_value=['git', 'python', 'docker'])


@pytest.fixture(autouse=True)
def history(mocker):
    return mocker.patch(
        'thefuck.rules.smart_command_suggestion.get_valid_history_without_current',
        return_value=['git status', 'python app.py'])


@pytest.mark.parametrize('script, output', [
    ('gti status', 'gti: command not found'),
    ('pythno app.py', 'pythno: not found'),
])
def test_match(mocker, script, output):
    mocker.patch(
        'thefuck.rules.smart_command_suggestion.which',
        return_value=None)
    assert match(Command(script, output))


def test_get_new_command(mocker):
    mocker.patch(
        'thefuck.rules.smart_command_suggestion.which',
        return_value=None)
    command = Command('pythno app.py', 'pythno: command not found')
    assert get_new_command(command)[0] == 'python app.py'


def test_does_not_match_existing_command(mocker):
    mocker.patch(
        'thefuck.rules.smart_command_suggestion.which',
        return_value='/usr/bin/python')
    command = Command('python app.py', 'python: command not found')
    assert not match(command)
