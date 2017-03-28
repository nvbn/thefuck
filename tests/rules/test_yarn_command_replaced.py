import pytest
from tests.utils import Command
from thefuck.rules.yarn_command_replaced import match, get_new_command


stderr = ('error `install` has been replaced with `add` to add new '
          'dependencies. Run "yarn add {}" instead.').format


@pytest.mark.parametrize('command', [
    Command(script='yarn install redux', stderr=stderr('redux')),
    Command(script='yarn install moment', stderr=stderr('moment')),
    Command(script='yarn install lodash', stderr=stderr('lodash'))])
def test_match(command):
    assert match(command)


@pytest.mark.parametrize('command', [
    Command('yarn install')])
def test_not_match(command):
    assert not match(command)


@pytest.mark.parametrize('command, new_command', [
    (Command('yarn install redux', stderr=stderr('redux')),
     'yarn add redux'),
    (Command('yarn install moment', stderr=stderr('moment')),
     'yarn add moment'),
    (Command('yarn install lodash', stderr=stderr('lodash')),
     'yarn add lodash')])
def test_get_new_command(command, new_command):
    assert get_new_command(command) == new_command
