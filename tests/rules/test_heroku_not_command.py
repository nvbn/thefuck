# -*- coding: utf-8 -*-

import pytest
from tests.utils import Command
from thefuck.rules.heroku_not_command import match, get_new_command


suggest_stderr = '''
 ▸    log is not a heroku command.
 ▸    Perhaps you meant logs?
 ▸    Run heroku _ to run heroku logs.
 ▸    Run heroku help for a list of available commands.'''


@pytest.mark.parametrize('cmd', ['log'])
def test_match(cmd):
    assert match(
        Command('heroku {}'.format(cmd), stderr=suggest_stderr))


@pytest.mark.parametrize('script, stderr', [
    ('cat log', suggest_stderr)])
def test_not_match(script, stderr):
    assert not match(Command(script, stderr=stderr))


@pytest.mark.parametrize('cmd, result', [
    ('log', 'heroku logs')])
def test_get_new_command(cmd, result):
    command = Command('heroku {}'.format(cmd), stderr=suggest_stderr)
    assert get_new_command(command) == result
