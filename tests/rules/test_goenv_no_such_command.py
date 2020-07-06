import pytest

from thefuck.rules.goenv_no_such_command import get_new_command, match
from thefuck.types import Command


@pytest.fixture
def output(goenv_cmd):
    return "goenv: no such command '{}'".format(goenv_cmd)


@pytest.mark.parametrize('script, goenv_cmd', [
    ('goenv globe', 'globe'),
    ('goenv intall 1.4.0', 'intall'),
    ('goenv list', 'list'),
])
def test_match(script, goenv_cmd, output):
    assert match(Command(script, output=output))


@pytest.mark.parametrize('script, output', [
    ('goenv global', 'system'),
    ('goenv versions', '  1.5.0\n  1.5.1\n* 1.5.2\n'),
    ('goenv install --list', '  1.5.0\n  1.5.1\n  1.5.2\n'),
])
def test_not_match(script, output):
    assert not match(Command(script, output=output))


@pytest.mark.parametrize('script, goenv_cmd, result', [
    ('goenv globe', 'globe', 'goenv global'),
    ('goenv intall 3.8.0', 'intall', 'goenv install 3.8.0'),
    ('goenv list', 'list', 'goenv install --list'),
    ('goenv remove 3.8.0', 'remove', 'goenv uninstall 3.8.0'),
])
def test_get_new_command(script, goenv_cmd, output, result):
    assert result in get_new_command(Command(script, output))
