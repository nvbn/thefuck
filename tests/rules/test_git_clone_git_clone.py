from thefuck.rules.git_clone_git_clone import match, get_new_command
from thefuck.types import Command


output_clean = """
fatal: Too many arguments.

usage: git clone [<options>] [--] <repo> [<dir>]
"""


def test_match():
    assert match(Command('git clone git clone foo', output_clean))


def test_not_match():
    assert not match(Command('', ''))
    assert not match(Command('git branch', ''))
    assert not match(Command('git clone foo', ''))
    assert not match(Command('git clone foo bar baz', output_clean))


def test_get_new_command():
    assert get_new_command(Command('git clone git clone foo', output_clean)) == 'git clone foo'
