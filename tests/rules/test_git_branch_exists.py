import pytest
from thefuck.rules.git_branch_exists import match, get_new_command
from thefuck.types import Command


@pytest.fixture
def output(src_branch_name):
    return "fatal: A branch named '{}' already exists.".format(src_branch_name)


@pytest.fixture
def new_command(branch_name):
    return [cmd.format(branch_name) for cmd in [
        'git branch -d {0} && git branch {0}',
        'git branch -d {0} && git checkout -b {0}',
        'git branch -D {0} && git branch {0}',
        'git branch -D {0} && git checkout -b {0}', 'git checkout {0}']]


@pytest.mark.parametrize('script, src_branch_name, branch_name', [
    ('git branch foo', 'foo', 'foo'),
    ('git checkout bar', 'bar', 'bar'),
    ('git checkout -b "let\'s-push-this"', '"let\'s-push-this"', '"let\'s-push-this"')])
def test_match(output, script, branch_name):
    assert match(Command(script, output))


@pytest.mark.parametrize('script', [
    'git branch foo',
    'git checkout bar',
    'git checkout -b "let\'s-push-this"'])
def test_not_match(script):
    assert not match(Command(script, ''))


@pytest.mark.parametrize('script, src_branch_name, branch_name', [
    ('git branch foo', 'foo', 'foo'),
    ('git checkout bar', 'bar', 'bar'),
    ('git checkout -b "let\'s-push-this"', "let's-push-this", "let\\'s-push-this")])
def test_get_new_command(output, new_command, script, src_branch_name, branch_name):
    assert get_new_command(Command(script, output)) == new_command
