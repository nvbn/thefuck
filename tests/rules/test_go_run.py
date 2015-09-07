import pytest
from thefuck.rules.go_run import match, get_new_command
from tests.utils import Command


@pytest.mark.parametrize('command', [
    Command(script='go run foo'),
    Command(script='go run bar')])
def test_match(command):
    assert match(command)


@pytest.mark.parametrize('command, new_command', [
    (Command('go run foo'), 'go run foo.go'),
    (Command('go run bar'), 'go run bar.go')])
def test_get_new_command(command, new_command):
    assert get_new_command(command) == new_command
