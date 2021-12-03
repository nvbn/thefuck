import pytest
from io import BytesIO
from thefuck.rules.git_checkout_master import (
    match, main_branch_exists, get_new_command
)
from thefuck.types import Command


def did_not_match(target, did_you_forget=False):
    error = ('error: pathspec \'{}\' did not match any file(s) known to git.'
             .format(target))

    if did_you_forget:
        error = ('{}\nDid you forget to \'git add\'?\''.format(error))

    return error


@pytest.fixture
def git_branch_patch(mocker, branches):
    mock = mocker.patch('subprocess.Popen')
    mock.return_value.stdout = BytesIO(branches)
    return mock


@pytest.mark.parametrize('command', [
    Command('git checkout master', did_not_match('master'))])
def test_match(command):
    assert match(command)


@pytest.mark.parametrize('command', [
    Command('git checkout master', did_not_match('master', True)),
    Command('git checkout -b master', ''),
    Command('git checkout known', '')])
def test_not_match(command):
    assert not match(command)


@pytest.mark.parametrize('branches', [
    b'* other\n  remotes/origin/HEAD -> origin/main\n  remotes/origin/main', ])
def test_main_branch_exists(branches, git_branch_patch):
    git_branch_patch(branches)
    assert main_branch_exists()


@pytest.mark.parametrize('branches', [
    b'',
    b'* not-master',
    b'* other\n  remotes/origin/HEAD -> origin/master'])
def test_not_main_branch_exists(branches, git_branch_patch):
    git_branch_patch(branches)
    assert not main_branch_exists()


@pytest.mark.parametrize('branches, command, new_command', [
    (b'* other\n  remotes/origin/HEAD -> origin/main\n  remotes/origin/main',
     Command('git checkout master', did_not_match('master')),
     'git checkout main'), ])
def test_get_new_command(branches, command, new_command, git_branch_patch):
    git_branch_patch(branches)
    assert get_new_command(command) == new_command
