from thefuck.rules.git_lfs_mistype import match, get_new_command
from thefuck.types import Command


def test_match():
    err_response = """
Error: unknown command "evn" for "git-lfs"

Did you mean this?
	env
	ext

Run 'git-lfs --help' for usage.
    """
    assert match(Command('git lfs evn', err_response))


def test_not_match():
    err_response = 'bash: git: command not found'
    assert not match(Command('git lfs env', err_response))


def test_not_git_command():
    err_response = """
Error: unknown command "evn" for "git-lfs"

Did you mean this?
	env
	ext

Run 'git-lfs --help' for usage.
    """
    assert not match(Command('docker lfs env', err_response))


def test_get_new_command():
    err_response = """
Error: unknown command "evn" for "git-lfs"

Did you mean this?
	env
	ext

Run 'git-lfs --help' for usage.
    """
    result = get_new_command(Command('git lfs evn', err_response))
    expected = 'git lfs env'
    assert result == expected


def test_get_another_new_command():
    err_response = """
Error: unknown command "chekout" for "git-lfs"

Did you mean this?
	checkout

Run 'git-lfs --help' for usage.
    """
    result = get_new_command(Command('git lfs chekout', err_response))
    expected = 'git lfs checkout'
    assert result == expected
