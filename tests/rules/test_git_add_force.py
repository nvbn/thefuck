import pytest
from thefuck.rules.git_add_force import match, get_new_command
from thefuck.types import Command


@pytest.fixture
def output():
    return ('The following paths are ignored by one of your .gitignore files:\n'
            'dist/app.js\n'
            'dist/background.js\n'
            'dist/options.js\n'
            'Use -f if you really want to add them.\n')


def test_match(output):
    assert match(Command('git add dist/*.js', output))
    assert not match(Command('git add dist/*.js', ''))


def test_get_new_command(output):
    assert (get_new_command(Command('git add dist/*.js', output))
            == "git add --force dist/*.js")
