import pytest
from thefuck.rules.git_merge_unrelated import match, get_new_command
from thefuck.types import Command


output = 'fatal: refusing to merge unrelated histories'


def test_match():
    assert match(Command('git merge test', output))
    assert not match(Command('git merge master', ''))
    assert not match(Command('ls', output))


@pytest.mark.parametrize('command, new_command', [
    (Command('git merge local', output),
     'git merge local --allow-unrelated-histories'),
    (Command('git merge -m "test" local', output),
     'git merge -m "test" local --allow-unrelated-histories'),
    (Command('git merge -m "test local" local', output),
     'git merge -m "test local" local --allow-unrelated-histories')])
def test_get_new_command(command, new_command):
    assert get_new_command(command) == new_command
