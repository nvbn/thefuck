import pytest
from thefuck.argument_parser import Parser
from thefuck.const import ARGUMENT_PLACEHOLDER


def _args(**override):
    args = {'alias': None, 'command': [], 'yes': False,
            'help': False, 'version': False, 'debug': False,
            'force_command': None, 'repeat': False}
    args.update(override)
    return args


@pytest.mark.parametrize('argv, result', [
    (['thefuck'], _args()),
    (['thefuck', '-a'], _args(alias='fuck')),
    (['thefuck', '-a', 'fix'], _args(alias='fix')),
    (['thefuck', 'git', 'branch', ARGUMENT_PLACEHOLDER, '-y'],
     _args(command=['git', 'branch'], yes=True)),
    (['thefuck', 'git', 'branch', '-a', ARGUMENT_PLACEHOLDER, '-y'],
     _args(command=['git', 'branch', '-a'], yes=True)),
    (['thefuck', ARGUMENT_PLACEHOLDER, '-v'], _args(version=True)),
    (['thefuck', ARGUMENT_PLACEHOLDER, '--help'], _args(help=True)),
    (['thefuck', 'git', 'branch', '-a', ARGUMENT_PLACEHOLDER, '-y', '-d'],
     _args(command=['git', 'branch', '-a'], yes=True, debug=True)),
    (['thefuck', 'git', 'branch', '-a', ARGUMENT_PLACEHOLDER, '-r', '-d'],
     _args(command=['git', 'branch', '-a'], repeat=True, debug=True))])
def test_parse(argv, result):
    assert vars(Parser().parse(argv)) == result
