import pytest
from thefuck.rules.sudo import match, get_new_command
from tests.utils import Command


@pytest.mark.parametrize('stderr', ['Permission denied',
                                    'permission denied',
                                    "npm ERR! Error: EACCES, unlink"])
def test_match(stderr):
    assert match(Command(stderr=stderr), None)


def test_not_match():
    assert not match(Command(), None)


def test_get_new_command():
    assert get_new_command(Command('ls'), None) == 'sudo ls'
