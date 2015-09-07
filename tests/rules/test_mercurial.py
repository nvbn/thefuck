import pytest

from tests.utils import Command
from thefuck.rules.mercurial import (
    extract_possibilities, match, get_new_command
)


@pytest.mark.parametrize('command', [
    Command('hg base', stderr=(
        "hg: unknown command 'base'"
        '\n(did you mean one of blame, phase, rebase?)'
    )),
    Command('hg branchch', stderr=(
        "hg: unknown command 'branchch'"
        '\n(did you mean one of branch, branches?)'
    )),
    Command('hg vert', stderr=(
        "hg: unknown command 'vert'"
        '\n(did you mean one of revert?)'
    )),
    Command('hg lgo -r tip', stderr=(
        "hg: command 're' is ambiguous:"
        '\n(did you mean one of log?)'
    )),
    Command('hg rerere', stderr=(
        "hg: unknown command 'rerere'"
        '\n(did you mean one of revert?)'
    )),
    Command('hg re', stderr=(
        "hg: command 're' is ambiguous:"
        '\n    rebase recover remove rename resolve revert'
    )),
    Command('hg re re', stderr=(
        "hg: command 're' is ambiguous:"
        '\n    rebase recover remove rename resolve revert'
    )),
])
def test_match(command):
    assert match(command)


@pytest.mark.parametrize('command', [
    Command('hg', stderr=(
        '\nMercurial Distributed SCM\n\nbasic commands:'
    )),
    Command('hg asdf', stderr=(
        "hg: unknown command 'asdf'"
        '\nMercurial Distributed SCM\n\nbasic commands:'
    )),
    Command('hg qwer', stderr=(
        "hg: unknown command 'qwer'"
        '\nMercurial Distributed SCM\n\nbasic commands:'
    )),
    Command('hg me', stderr=(
        "\nabort: no repository found in './thefuck' (.hg not found)!"
    )),
    Command('hg reb', stderr=(
        "\nabort: no repository found in './thefuck' (.hg not found)!"
    )),
    Command('hg co', stderr=(
        "\nabort: no repository found in './thefuck' (.hg not found)!"
    )),
])
def test_not_match(command):
    assert not match(command)


@pytest.mark.parametrize('command, possibilities', [
    (Command('hg base', stderr=(
        "hg: unknown command 'base'"
        '\n(did you mean one of blame, phase, rebase?)'
    )), ['blame', 'phase', 'rebase']),
    (Command('hg branchch', stderr=(
        "hg: unknown command 'branchch'"
        '\n(did you mean one of branch, branches?)'
    )), ['branch', 'branches']),
    (Command('hg vert', stderr=(
        "hg: unknown command 'vert'"
        '\n(did you mean one of revert?)'
    )), ['revert']),
    (Command('hg lgo -r tip', stderr=(
        "hg: command 're' is ambiguous:"
        '\n(did you mean one of log?)'
    )), ['log']),
    (Command('hg rerere', stderr=(
        "hg: unknown command 'rerere'"
        '\n(did you mean one of revert?)'
    )), ['revert']),
    (Command('hg re', stderr=(
        "hg: command 're' is ambiguous:"
        '\n    rebase recover remove rename resolve revert'
    )), ['rebase', 'recover', 'remove', 'rename', 'resolve', 'revert']),
    (Command('hg re re', stderr=(
        "hg: command 're' is ambiguous:"
        '\n    rebase recover remove rename resolve revert'
    )), ['rebase', 'recover', 'remove', 'rename', 'resolve', 'revert']),
])
def test_extract_possibilities(command, possibilities):
    assert extract_possibilities(command) == possibilities


@pytest.mark.parametrize('command, new_command', [
    (Command('hg base', stderr=(
        "hg: unknown command 'base'"
        '\n(did you mean one of blame, phase, rebase?)'
    )), 'hg rebase'),
    (Command('hg branchch', stderr=(
        "hg: unknown command 'branchch'"
        '\n(did you mean one of branch, branches?)'
    )), 'hg branch'),
    (Command('hg vert', stderr=(
        "hg: unknown command 'vert'"
        '\n(did you mean one of revert?)'
    )), 'hg revert'),
    (Command('hg lgo -r tip', stderr=(
        "hg: command 're' is ambiguous:"
        '\n(did you mean one of log?)'
    )), 'hg log -r tip'),
    (Command('hg rerere', stderr=(
        "hg: unknown command 'rerere'"
        '\n(did you mean one of revert?)'
    )), 'hg revert'),
    (Command('hg re', stderr=(
        "hg: command 're' is ambiguous:"
        '\n    rebase recover remove rename resolve revert'
    )), 'hg rebase'),
    (Command('hg re re', stderr=(
        "hg: command 're' is ambiguous:"
        '\n    rebase recover remove rename resolve revert'
    )), 'hg rebase re'),
])
def test_get_new_command(command, new_command):
    assert get_new_command(command) == new_command
