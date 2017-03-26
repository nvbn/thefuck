# -*- encoding: utf-8 -*-

from io import BytesIO
import pytest
from tests.utils import Command
from thefuck.rules.yarn_command_replaced import match, get_new_command


stderr = '''
error `install` has been replaced with `add` to add new dependencies. Run "yarn add {}" instead.
'''.format


@pytest.mark.parametrize('command', [
    Command(script='yarn install asdklj', stderr=stderr('asdklj')),
    Command(script='yarn install liuqowe', stderr=stderr('liuqowe')),
    Command(script='yarn install zxmnc', stderr=stderr('zxmnc'))])
def test_match(command):
    assert match(command)


@pytest.mark.parametrize('command, new_command', [
    (Command('yarn install asdklj', stderr=stderr('asdklj')), 'yarn add asdklj'),
    (Command('yarn install iiuqowe', stderr=stderr('iiuqowe')), 'yarn add iiuqowe'),
    (Command('yarn install zxmnc', stderr=stderr('zxmnc')), 'yarn add zxmnc')])
def test_get_new_command(command, new_command):
    assert get_new_command(command) == new_command
