import pytest

from thefuck.rules.nodenv_no_such_command import get_new_command, match
from thefuck.types import Command


@pytest.fixture
def output(nodenv_cmd):
    return "nodenv: no such command `{}'".format(nodenv_cmd)


@pytest.mark.parametrize('script, nodenv_cmd', [
    ('nodenv globe', 'globe'),
    ('nodenv intall 3.8.0', 'intall'),
    ('nodenv list', 'list'),
])
def test_match(script, nodenv_cmd, output):
    assert match(Command(script, output=output))


@pytest.mark.parametrize('script, output', [
    ('nodenv global', 'system'),
    ('nodenv versions', '  3.7.0\n  3.7.1\n* 3.7.2\n'),
    ('nodenv install --list', '  3.7.0\n  3.7.1\n  3.7.2\n'),
])
def test_not_match(script, output):
    assert not match(Command(script, output=output))
