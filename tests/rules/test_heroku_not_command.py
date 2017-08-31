# -*- coding: utf-8 -*-

import pytest
from thefuck.types import Command
from thefuck.rules.heroku_not_command import match, get_new_command


suggest_output = '''
 ▸    log is not a heroku command.
 ▸    Perhaps you meant logs?
 ▸    Run heroku _ to run heroku logs.
 ▸    Run heroku help for a list of available commands.'''


@pytest.mark.parametrize('cmd', ['log'])
def test_match(cmd):
    assert match(
        Command('heroku {}'.format(cmd), suggest_output))


@pytest.mark.parametrize('script, output', [
    ('cat log', suggest_output)])
def test_not_match(script, output):
    assert not match(Command(script, output))


@pytest.mark.parametrize('cmd, result', [
    ('log', 'heroku logs')])
def test_get_new_command(cmd, result):
    command = Command('heroku {}'.format(cmd), suggest_output)
    assert get_new_command(command) == result
