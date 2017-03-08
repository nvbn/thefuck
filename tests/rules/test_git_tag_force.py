import pytest
from thefuck.rules.git_tag_force import match, get_new_command
from tests.utils import Command


@pytest.fixture
def stderr():
    return '''fatal: tag 'alert' already exists'''


def test_match(stderr):
    assert match(Command('git tag alert', stderr=stderr))
    assert not match(Command('git tag alert'))


def test_get_new_command(stderr):
    assert get_new_command(Command('git tag alert', stderr=stderr)) \
           == "git tag --force alert"
