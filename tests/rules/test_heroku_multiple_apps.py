# -*- coding: utf-8 -*-

import pytest
from thefuck.types import Command
from thefuck.rules.heroku_multiple_apps import match, get_new_command


suggest_output = '''
 ▸    Multiple apps in git remotes
 ▸    Usage: --remote heroku-dev
 ▸    or: --app myapp-dev
 ▸    Your local git repository has more than 1 app referenced in git remotes.
 ▸    Because of this, we can't determine which app you want to run this command against.
 ▸    Specify the app you want with --app or --remote.
 ▸    Heroku remotes in repo:
 ▸    myapp (heroku)
 ▸    myapp-dev (heroku-dev)
 ▸
 ▸    https://devcenter.heroku.com/articles/multiple-environments
'''

not_match_output = '''
=== HEROKU_POSTGRESQL_TEAL_URL, DATABASE_URL
Plan:                  Hobby-basic
Status:                Available
Connections:           20/20
PG Version:            9.6.4
Created:               2017-01-01 00:00 UTC
Data Size:             99.9 MB
Tables:                99
Rows:                  12345/10000000 (In compliance)
Fork/Follow:           Unsupported
Rollback:              Unsupported
Continuous Protection: Off
Add-on:                postgresql-round-12345
'''


@pytest.mark.parametrize('cmd', ['pg'])
def test_match(cmd):
    assert match(
        Command('heroku {}'.format(cmd), suggest_output))


@pytest.mark.parametrize('script, output', [
    ('heroku pg', not_match_output)])
def test_not_match(script, output):
    assert not match(Command(script, output))


@pytest.mark.parametrize('cmd, result', [
    ('pg', ['heroku pg --app myapp', 'heroku pg --app myapp-dev'])])
def test_get_new_command(cmd, result):
    command = Command('heroku {}'.format(cmd), suggest_output)
    assert get_new_command(command) == result
