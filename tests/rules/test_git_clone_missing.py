import pytest
from itertools import product
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

# TODO: Powershell,
shell_errors = [
    'not found',  # sh
    'command not found',  # fish
    'No such file or directory',  # bash
    'no such file or directory',  # zsh
    'is not recognized as',  # cmd, powershell
]



@pytest.mark.parametrize(
    'cmd',
    [Command(c, e) for c, e in product(valid_urls, shell_errors)]
)
def test_match(cmd):
    print(cmd)
    assert match(cmd)


@pytest.mark.parametrize(
    'cmd',
    [Command(c, shell_errors[0]) for c in invalid_urls]
)
def test_not_match(cmd):
    print(cmd)
    assert not match(cmd)


@pytest.mark.parametrize(
    'cmd',
    [Command(c, shell_errors[0]) for c in valid_urls]
)
def test_get_new_command(cmd):
    print(cmd)
    assert get_new_command(cmd) == 'git clone ' + cmd.script
