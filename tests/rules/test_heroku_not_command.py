import pytest
from tests.utils import Command
from thefuck.rules.heroku_not_command import match, get_new_command


def suggest_stderr(cmd):
    return ''' !    `{}` is not a heroku command.
     !    Perhaps you meant `logs`, `pg`.
     !    See `heroku help` for a list of available commands.'''.format(cmd)


no_suggest_stderr = ''' !    `aaaaa` is not a heroku command.
 !    See `heroku help` for a list of available commands.'''


@pytest.mark.parametrize('cmd', ['log', 'pge'])
def test_match(cmd):
    assert match(
        Command('heroku {}'.format(cmd), stderr=suggest_stderr(cmd)))


@pytest.mark.parametrize('script, stderr', [
    ('cat log', suggest_stderr('log')),
    ('heroku aaa', no_suggest_stderr)])
def test_not_match(script, stderr):
    assert not match(Command(script, stderr=stderr))


@pytest.mark.parametrize('cmd, result', [
    ('log', ['heroku logs', 'heroku pg']),
    ('pge', ['heroku pg', 'heroku logs'])])
def test_get_new_command(cmd, result):
    command = Command('heroku {}'.format(cmd), stderr=suggest_stderr(cmd))
    assert get_new_command(command) == result
