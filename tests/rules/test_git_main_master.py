import pytest
from thefuck.rules.git_main_master import match, get_new_command
from thefuck.types import Command


output = 'error: pathspec \'%s\' did not match any file(s) known to git'


def test_match():
    assert match(Command('git checkout main', output % ('main')))
    assert match(Command('git checkout master', output % ('master')))
    assert not match(Command('git checkout master', ''))
    assert not match(Command('git checkout main', ''))
    assert not match(Command('git checkout wibble', output % ('wibble')))


@pytest.mark.parametrize('command, new_command', [
    (Command('git checkout main', output % ('main')),
     'git checkout master'),
    (Command('git checkout master', output % ('master')),
     'git checkout main')])
def test_get_new_command(command, new_command):
    assert get_new_command(command) == new_command
