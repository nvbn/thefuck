from thefuck.rules.git_clone_git_clone import match, get_new_command
from thefuck.types import Command

output_clean = """
fatal: Too many arguments.

usage: git clone [<options>] [--] <repo> [<dir>]
"""

http_url = 'https://github.com/nvbn/thefuck.git'
ssh_url = 'git@github.com:nvbn/thefuck.git'

# HELP WANTED: How can I make this independent of the shell?
http_output = """
bash: https://github.com/nvbn/thefuck.git: No such file or directory
"""
ssh_output = """
bash: hgit@github.com:nvbn/thefuck.git: No such file or directory
"""


def test_match():
    assert match(Command(http_url, http_output))
    assert match(Command(ssh_url, ssh_output))


def test_not_match():
    assert not match(Command('', ''))
    assert not match(Command('git branch', ''))
    assert not match(Command('git clone foo', ''))
    assert not match(Command('git clone foo bar baz', output_clean))
    assert not match(Command('git clone ' + http_url, ''))


def test_get_new_command():
    assert get_new_command(Command(http_url, http_output)) == 'git clone ' + http_url
    assert get_new_command(Command(ssh_url, ssh_output)) == 'git clone ' + ssh_url
