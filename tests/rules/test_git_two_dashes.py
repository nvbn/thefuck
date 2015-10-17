import pytest
from thefuck.rules.git_two_dashes import match, get_new_command
from tests.utils import Command


@pytest.fixture
def stderr(meant):
    return 'error: did you mean `%s` (with two dashes ?)' % meant


@pytest.mark.parametrize('command', [
    Command(script='git add -patch', stderr=stderr('--patch')),
    Command(script='git checkout -patch', stderr=stderr('--patch')),
    Command(script='git commit -amend', stderr=stderr('--amend')),
    Command(script='git push -tags', stderr=stderr('--tags')),
    Command(script='git rebase -continue', stderr=stderr('--continue'))])
def test_match(command):
    assert match(command)


@pytest.mark.parametrize('command', [
    Command(script='git add --patch'),
    Command(script='git checkout --patch'),
    Command(script='git commit --amend'),
    Command(script='git push --tags'),
    Command(script='git rebase --continue')])
def test_not_match(command):
    assert not match(command)


@pytest.mark.parametrize('command, output', [
    (Command(script='git add -patch', stderr=stderr('--patch')),
        'git add --patch'),
    (Command(script='git checkout -patch', stderr=stderr('--patch')),
        'git checkout --patch'),
    (Command(script='git checkout -patch', stderr=stderr('--patch')),
        'git checkout --patch'),
    (Command(script='git init -bare', stderr=stderr('--bare')),
        'git init --bare'),
    (Command(script='git commit -amend', stderr=stderr('--amend')),
        'git commit --amend'),
    (Command(script='git push -tags', stderr=stderr('--tags')),
        'git push --tags'),
    (Command(script='git rebase -continue', stderr=stderr('--continue')),
        'git rebase --continue')])
def test_get_new_command(command, output):
    assert get_new_command(command) == output
