import pytest
from thefuck.rules.yarn_alias import match, get_new_command
from tests.utils import Command


stderr_remove = 'error Did you mean `yarn remove`?'
stderr_etl = 'error Command "etil" not found. Did you mean "etl"?'
stderr_list = 'error Did you mean `yarn list`?'


@pytest.mark.parametrize('command', [
    Command(script='yarn rm', stderr=stderr_remove),
    Command(script='yarn etil', stderr=stderr_etl),
    Command(script='yarn ls', stderr=stderr_list)])
def test_match(command):
    assert match(command)


@pytest.mark.parametrize('command, new_command', [
    (Command('yarn rm', stderr=stderr_remove), 'yarn remove'),
    (Command('yarn etil', stderr=stderr_etl), 'yarn etl'),
    (Command('yarn ls', stderr=stderr_list), 'yarn list')])
def test_get_new_command(command, new_command):
    assert get_new_command(command) == new_command
