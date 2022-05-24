import pytest
from thefuck.rules.git_clone_missing import match, get_new_command
from thefuck.types import Command

https_url = 'https://github.com/nvbn/thefuck.git'
http_url = 'http://github.com/nvbn/thefuck.git'
ssh_url = 'git@github.com:nvbn/thefuck.git'

# HELP WANTED: How can I make this independent of the shell?
https_output = """
bash: https://github.com/nvbn/thefuck.git: No such file or directory
"""
http_output = """
bash: https://github.com/nvbn/thefuck.git: No such file or directory
"""
ssh_output = """
bash: git@github.com:nvbn/thefuck.git: No such file or directory
"""

@pytest.mark.parametrize(
    'cmd', [
        Command(https_url, https_output),
        Command(http_url, http_output),
        Command(ssh_url, ssh_output),
    ]
)
def test_match(cmd):
    assert match(cmd)

@pytest.mark.parametrize(
    'cmd', [
        Command('', ''),
        Command('git branch', ''),
        Command('git clone foo', ''),
        Command('git clone foo bar baz', ''),
        Command('git clone ' + http_url, http_output),
        Command('git@example.com:thing.gut', ssh_output),
        Command('https:/github.com/nvbn/thefuck.git', http_output),
    ]
)
def test_not_match(cmd):
    assert not match(cmd)


@pytest.mark.parametrize(
    'cmd', [
        Command(https_url, https_output),
        Command(http_url, http_output),
        Command(ssh_url, ssh_output),
    ]
)
def test_get_new_command(cmd):
    assert get_new_command(cmd) == 'git clone ' + cmd.script
