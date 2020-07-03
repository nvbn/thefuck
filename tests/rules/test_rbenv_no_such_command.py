import pytest

from thefuck.rules.rbenv_no_such_command import match
from thefuck.types import Command


@pytest.fixture
def output(rbenv_cmd):
    return "rbenv: no such command `{}'".format(rbenv_cmd)


@pytest.mark.parametrize('script, rbenv_cmd', [
    ('rbenv globe', 'globe'),
    ('rbenv intall 3.8.0', 'intall'),
    ('rbenv list', 'list'),
])
def test_match(script, rbenv_cmd, output):
    assert match(Command(script, output=output))


@pytest.mark.parametrize('script, output', [
    ('rbenv global', 'system'),
    ('rbenv versions', '  3.7.0\n  3.7.1\n* 3.7.2\n'),
    ('rbenv install --list', '  3.7.0\n  3.7.1\n  3.7.2\n'),
])
def test_not_match(script, output):
    assert not match(Command(script, output=output))
