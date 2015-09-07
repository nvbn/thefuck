import pytest
from thefuck.rules.dry import match, get_new_command
from tests.utils import Command


@pytest.mark.parametrize('command', [
    Command(script='cd cd foo'),
    Command(script='git git push origin/master')])
def test_match(command):
    assert match(command)


@pytest.mark.parametrize('command, new_command', [
    (Command('cd cd foo'), 'cd foo'),
    (Command('git git push origin/master'), 'git push origin/master')])
def test_get_new_command(command, new_command):
    assert get_new_command(command) == new_command
