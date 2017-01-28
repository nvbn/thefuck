import pytest
from thefuck.rules.git_add_force import match, get_new_command
from tests.utils import Command


@pytest.fixture
def stderr():
    return ('The following paths are ignored by one of your .gitignore files:\n'
            'dist/app.js\n'
            'dist/background.js\n'
            'dist/options.js\n'
            'Use -f if you really want to add them.\n')


def test_match(stderr):
    assert match(Command('git add dist/*.js', stderr=stderr))
    assert not match(Command('git add dist/*.js'))


def test_get_new_command(stderr):
    assert get_new_command(Command('git add dist/*.js', stderr=stderr)) \
           == "git add --force dist/*.js"
