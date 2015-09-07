import pytest
from thefuck.rules.git_stash import match, get_new_command
from tests.utils import Command


cherry_pick_error = (
        'error: Your local changes would be overwritten by cherry-pick.\n'
        'hint: Commit your changes or stash them to proceed.\n'
        'fatal: cherry-pick failed')


rebase_error = (
        'Cannot rebase: Your index contains uncommitted changes.\n'
        'Please commit or stash them.')


@pytest.mark.parametrize('command', [
    Command(script='git cherry-pick a1b2c3d', stderr=cherry_pick_error),
    Command(script='git rebase -i HEAD~7', stderr=rebase_error)])
def test_match(command):
    assert match(command)


@pytest.mark.parametrize('command', [
    Command(script='git cherry-pick a1b2c3d', stderr=('')),
    Command(script='git rebase -i HEAD~7', stderr=(''))])
def test_not_match(command):
    assert not match(command)


@pytest.mark.parametrize('command, new_command', [
    (Command(script='git cherry-pick a1b2c3d', stderr=cherry_pick_error),
     'git stash && git cherry-pick a1b2c3d'),
    (Command('git rebase -i HEAD~7', stderr=rebase_error),
     'git stash && git rebase -i HEAD~7')])
def test_get_new_command(command, new_command):
    assert get_new_command(command) == new_command
