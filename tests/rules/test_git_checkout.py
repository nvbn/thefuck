import pytest
from io import BytesIO
from thefuck.rules.git_checkout import match, get_branches, get_new_command
from tests.utils import Command


@pytest.fixture
def did_not_match(target, did_you_forget=False):
    error = ("error: pathspec '{}' did not match any "
             "file(s) known to git.".format(target))
    if did_you_forget:
        error = ("{}\nDid you forget to 'git add'?'".format(error))
    return error


@pytest.fixture
def git_branch(mocker, branches):
    mock = mocker.patch('subprocess.Popen')
    mock.return_value.stdout = BytesIO(branches)
    return mock


@pytest.mark.parametrize('command', [
    Command(script='git checkout unknown', stderr=did_not_match('unknown')),
    Command(script='git commit unknown', stderr=did_not_match('unknown'))])
def test_match(command):
    assert match(command)


@pytest.mark.parametrize('command', [
    Command(script='git submodule update unknown',
            stderr=did_not_match('unknown', True)),
    Command(script='git checkout known', stderr=('')),
    Command(script='git commit known', stderr=(''))])
def test_not_match(command):
    assert not match(command)


@pytest.mark.parametrize('branches, branch_list', [
    (b'', []),
    (b'* master', ['master']),
    (b'  remotes/origin/master', ['master']),
    (b'  just-another-branch', ['just-another-branch']),
    (b'* master\n  just-another-branch', ['master', 'just-another-branch']),
    (b'* master\n  remotes/origin/master\n  just-another-branch',
     ['master', 'master', 'just-another-branch'])])
def test_get_branches(branches, branch_list, git_branch):
    git_branch(branches)
    assert list(get_branches()) == branch_list


@pytest.mark.parametrize('branches, command, new_command', [
    (b'',
     Command(script='git checkout unknown', stderr=did_not_match('unknown')),
     'git branch unknown && git checkout unknown'),
    (b'',
     Command('git commit unknown', stderr=did_not_match('unknown')),
     'git branch unknown && git commit unknown'),
    (b'  test-random-branch-123',
     Command(script='git checkout tst-rdm-brnch-123',
             stderr=did_not_match('tst-rdm-brnch-123')),
     'git checkout test-random-branch-123'),
    (b'  test-random-branch-123',
     Command(script='git commit tst-rdm-brnch-123',
             stderr=did_not_match('tst-rdm-brnch-123')),
     'git commit test-random-branch-123')])
def test_get_new_command(branches, command, new_command, git_branch):
    git_branch(branches)
    assert get_new_command(command) == new_command
