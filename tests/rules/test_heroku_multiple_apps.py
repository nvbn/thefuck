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


@pytest.mark.parametrize('cmd', ['pg'])
def test_match(cmd):
    assert match(
        Command('heroku {}'.format(cmd), suggest_output))


# TODO
# @pytest.mark.parametrize('script, output', [
#     ('cat log', suggest_output)])
# def test_not_match(script, output):
#     assert not match(Command(script, output))


@pytest.mark.parametrize('cmd, result', [
    ('pg', ['heroku pg --app myapp', 'heroku pg --app myapp-dev'])])
def test_get_new_command(cmd, result):
    command = Command('heroku {}'.format(cmd), suggest_output)
    assert get_new_command(command) == result
