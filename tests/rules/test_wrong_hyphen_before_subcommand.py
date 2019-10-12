import pytest

from thefuck.rules.wrong_hyphen_before_subcommand import match, get_new_command
from thefuck.types import Command

@pytest.fixture(autouse=True)
def get_all_executables(mocker):
    mocker.patch('thefuck.rules.wrong_hyphen_before_subcommand.get_all_executables',
        return_value=['git', 'apt', 'apt-get', 'ls', 'pwd'])


@pytest.mark.parametrize('script', [
    'ls-la',
    'git-log',
    'apt-install python'])
def test_match(mocker, script):
    assert match(Command(script, ""))


@pytest.mark.parametrize('script, result', [
    ('ls-la', 'ls -la'),
    ('git-log', 'git log'),
    ('apt-install python', 'apt install python')])
def test_get_new_command(mocker, script, result):
    assert get_new_command(Command(script, "")) == result


@pytest.mark.parametrize('script', [
    'ls la',
    'git-make',
    'apt-get python'])
def test_not_match(mocker, script):
    assert not match(Command(script, ""))
