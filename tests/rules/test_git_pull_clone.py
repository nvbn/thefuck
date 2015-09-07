import pytest
from thefuck.rules.git_pull_clone import match, get_new_command
from tests.utils import Command


git_err = '''
fatal: Not a git repository (or any parent up to mount point /home)
Stopping at filesystem boundary (GIT_DISCOVERY_ACROSS_FILESYSTEM not set).
'''


@pytest.mark.parametrize('command', [
    Command(script='git pull git@github.com:mcarton/thefuck.git', stderr=git_err)])
def test_match(command):
    assert match(command)


@pytest.mark.parametrize('command, output', [
    (Command(script='git pull git@github.com:mcarton/thefuck.git', stderr=git_err), 'git clone git@github.com:mcarton/thefuck.git')])
def test_get_new_command(command, output):
    assert get_new_command(command) == output
