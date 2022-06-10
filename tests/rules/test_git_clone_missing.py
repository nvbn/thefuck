import pytest
from thefuck.rules.git_clone_missing import match, get_new_command
from thefuck.types import Command

valid_urls = [
    'https://github.com/nvbn/thefuck.git',
    'https://github.com/nvbn/thefuck',
    'http://github.com/nvbn/thefuck.git',
    'git@github.com:nvbn/thefuck.git',
    'git@github.com:nvbn/thefuck',
    'ssh://git@github.com:nvbn/thefuck.git',
]
invalid_urls = [
    '',  # No command
    'notacommand',  # Command not found
    'git clone foo',  # Valid clone
    'git clone https://github.com/nvbn/thefuck.git',  # Full command
    'github.com/nvbn/thefuck.git',  # Missing protocol
    'github.com:nvbn/thefuck.git',  # SSH missing username
    'git clone git clone ssh://git@github.com:nvbn/thefrick.git',  # Double clone
    'https:/github.com/nvbn/thefuck.git'  # Bad protocol
]


@pytest.mark.parametrize(
    'cmd',
    [Command(c, 'not found') for c in valid_urls]
)
def test_match(cmd):
    assert match(cmd)


@pytest.mark.parametrize(
    'cmd',
    [Command(c, 'not found') for c in invalid_urls]
)
def test_not_match(cmd):
    assert not match(cmd)


@pytest.mark.parametrize(
    'cmd',
    [Command(c, 'not found') for c in valid_urls]
)
def test_get_new_command(cmd):
    assert get_new_command(cmd) == 'git clone ' + cmd.script
