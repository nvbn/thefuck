import pytest
from theheck.argument_parser import Parser
from theheck.const import ARGUMENT_PLACEHOLDER


def _args(**override):
    args = {'alias': None, 'command': [], 'yes': False,
            'help': False, 'version': False, 'debug': False,
            'force_command': None, 'repeat': False,
            'enable_experimental_instant_mode': False,
            'shell_logger': None}
    args.update(override)
    return args


@pytest.mark.parametrize('argv, result', [
    (['theheck'], _args()),
    (['theheck', '-a'], _args(alias='heck')),
    (['theheck', '--alias', '--enable-experimental-instant-mode'],
     _args(alias='heck', enable_experimental_instant_mode=True)),
    (['theheck', '-a', 'fix'], _args(alias='fix')),
    (['theheck', 'git', 'branch', ARGUMENT_PLACEHOLDER, '-y'],
     _args(command=['git', 'branch'], yes=True)),
    (['theheck', 'git', 'branch', '-a', ARGUMENT_PLACEHOLDER, '-y'],
     _args(command=['git', 'branch', '-a'], yes=True)),
    (['theheck', ARGUMENT_PLACEHOLDER, '-v'], _args(version=True)),
    (['theheck', ARGUMENT_PLACEHOLDER, '--help'], _args(help=True)),
    (['theheck', 'git', 'branch', '-a', ARGUMENT_PLACEHOLDER, '-y', '-d'],
     _args(command=['git', 'branch', '-a'], yes=True, debug=True)),
    (['theheck', 'git', 'branch', '-a', ARGUMENT_PLACEHOLDER, '-r', '-d'],
     _args(command=['git', 'branch', '-a'], repeat=True, debug=True)),
    (['theheck', '-l', '/tmp/log'], _args(shell_logger='/tmp/log')),
    (['theheck', '--shell-logger', '/tmp/log'],
     _args(shell_logger='/tmp/log'))])
def test_parse(argv, result):
    assert vars(Parser().parse(argv)) == result
