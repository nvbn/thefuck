import pytest
from thefuck.rules.git_branch_exists import match, get_new_command
from tests.utils import Command


@pytest.fixture
def stderr(branch_name):
    return "fatal: A branch named '{}' already exists.".format(branch_name)


@pytest.fixture
def new_command(branch_name):
    return [cmd.format(branch_name) for cmd in [
        'git branch -d {0} && git branch {0}',
        'git branch -d {0} && git checkout -b {0}',
        'git branch -D {0} && git branch {0}',
        'git branch -D {0} && git checkout -b {0}', 'git checkout {0}']]


@pytest.mark.parametrize('script, branch_name', [
    ('git branch foo', 'foo'), ('git checkout bar', 'bar')])
def test_match(stderr, script, branch_name):
    assert match(Command(script=script, stderr=stderr))


@pytest.mark.parametrize('script', ['git branch foo', 'git checkout bar'])
def test_not_match(script):
    assert not match(Command(script=script, stderr=''))


@pytest.mark.parametrize('script, branch_name, ', [
    ('git branch foo', 'foo'), ('git checkout bar', 'bar')])
def test_get_new_command(stderr, new_command, script, branch_name):
    assert get_new_command(Command(script=script, stderr=stderr)) == new_command
