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
    'ssh git@github.com:nvbn/thefrick.git',  # ssh command, not a git clone
    'git clone foo',  # Valid clone
    'git clone https://github.com/nvbn/thefuck.git',  # Full command
    'github.com/nvbn/thefuck.git',  # Missing protocol
    'github.com:nvbn/thefuck.git',  # SSH missing username
    'git clone git clone ssh://git@github.com:nvbn/thefrick.git',  # 2x clone
    'https:/github.com/nvbn/thefuck.git'  # Bad protocol
]
outputs = [
    'No such file or directory',
    'not found',
    'is not recognised as',
]


@pytest.mark.parametrize('cmd', valid_urls)
@pytest.mark.parametrize('output', outputs)
def test_match(cmd, output):
    c = Command(cmd, output)
    assert match(c)


@pytest.mark.parametrize('cmd', invalid_urls)
@pytest.mark.parametrize('output', outputs + ["some other output"])
def test_not_match(cmd, output):
    c = Command(cmd, output)
    assert not match(c)


@pytest.mark.parametrize('script', valid_urls)
@pytest.mark.parametrize('output', outputs)
def test_get_new_command(script, output):
    command = Command(script, output)
    new_command = 'git clone ' + script
    assert get_new_command(command) == new_command
