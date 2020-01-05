import pytest

from thefuck.rules.az_cli import match, get_new_command
from thefuck.types import Command


no_suggestions = '''\
az provider: error: the following arguments are required: _subcommand
usage: az provider [-h] {list,show,register,unregister,operation} ...
'''


misspelled_command = '''\
az: 'providers' is not in the 'az' command group. See 'az --help'.

The most similar choice to 'providers' is:
    provider
'''

misspelled_subcommand = '''\
az provider: 'lis' is not in the 'az provider' command group. See 'az provider --help'.

The most similar choice to 'lis' is:
    list
'''


@pytest.mark.parametrize('command', [
    Command('az providers', misspelled_command),
    Command('az provider lis', misspelled_subcommand)])
def test_match(command):
    assert match(command)


def test_not_match():
    assert not match(Command('az provider', no_suggestions))


@pytest.mark.parametrize('command, result', [
    (Command('az providers list', misspelled_command), ['az provider list']),
    (Command('az provider lis', misspelled_subcommand), ['az provider list'])
])
def test_get_new_command(command, result):
    assert get_new_command(command) == result
