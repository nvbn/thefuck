import pytest

from thefuck.rules.pyenv_no_such_command import match
from thefuck.types import Command


@pytest.fixture
def output(pyenv_cmd):
    return "pyenv: no such command `{}'".format(pyenv_cmd)


@pytest.mark.parametrize('script, pyenv_cmd', [
    ('pyenv globe', 'globe'),
    ('pyenv intall 3.8.0', 'intall'),
    ('pyenv list', 'list'),
])
def test_match(script, pyenv_cmd, output):
    assert match(Command(script, output=output))


@pytest.mark.parametrize('script, output', [
    ('pyenv global', 'system'),
    ('pyenv versions', '  3.7.0\n  3.7.1\n* 3.7.2\n'),
    ('pyenv install --list', '  3.7.0\n  3.7.1\n  3.7.2\n'),
])
def test_not_match(script, output):
    assert not match(Command(script, output=output))
