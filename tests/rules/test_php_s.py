import pytest
from thefuck.rules.php_s import get_new_command, match
from thefuck.types import Command


def test_match():
    assert match(Command('php -s localhost:8000', ''))


@pytest.mark.parametrize('command', [
    Command('php -S localhost:8000', ''),
    Command('vim php -s', '')
])
def test_not_match(command):
    assert not match(command)


def test_get_new_command():
    new_command = get_new_command(Command('php -s localhost:8000', ''))
    assert new_command == 'php -S localhost:8000'
