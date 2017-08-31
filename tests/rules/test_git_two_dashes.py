import pytest
from thefuck.rules.git_two_dashes import match, get_new_command
from thefuck.types import Command


output = 'error: did you mean `{}` (with two dashes ?)'.format


@pytest.mark.parametrize('command', [
    Command('git add -patch', output('--patch')),
    Command('git checkout -patch', output('--patch')),
    Command('git commit -amend', output('--amend')),
    Command('git push -tags', output('--tags')),
    Command('git rebase -continue', output('--continue'))])
def test_match(command):
    assert match(command)


@pytest.mark.parametrize('command', [
    Command('git add --patch', ''),
    Command('git checkout --patch', ''),
    Command('git commit --amend', ''),
    Command('git push --tags', ''),
    Command('git rebase --continue', '')])
def test_not_match(command):
    assert not match(command)


@pytest.mark.parametrize('command, output', [
    (Command('git add -patch', output('--patch')),
        'git add --patch'),
    (Command('git checkout -patch', output('--patch')),
        'git checkout --patch'),
    (Command('git checkout -patch', output('--patch')),
        'git checkout --patch'),
    (Command('git init -bare', output('--bare')),
        'git init --bare'),
    (Command('git commit -amend', output('--amend')),
        'git commit --amend'),
    (Command('git push -tags', output('--tags')),
        'git push --tags'),
    (Command('git rebase -continue', output('--continue')),
        'git rebase --continue')])
def test_get_new_command(command, output):
    assert get_new_command(command) == output
