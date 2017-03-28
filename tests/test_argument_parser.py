import pytest
from thefuck.argument_parser import Parser
from thefuck.const import ARGUMENT_PLACEHOLDER


@pytest.mark.parametrize('argv, result', [
    (['thefuck'], {'alias': None, 'command': [], 'yes': False,
                   'help': False, 'version': False}),
    (['thefuck', '-a'], {'alias': 'fuck', 'command': [], 'yes': False,
                         'help': False, 'version': False}),
    (['thefuck', '-a', 'fix'], {'alias': 'fix', 'command': [], 'yes': False,
                                'help': False, 'version': False}),
    (['thefuck', 'git', 'branch', ARGUMENT_PLACEHOLDER, '-y'],
     {'alias': None, 'command': ['git', 'branch'], 'yes': True,
      'help': False, 'version': False}),
    (['thefuck', 'git', 'branch', '-a', ARGUMENT_PLACEHOLDER, '-y'],
     {'alias': None, 'command': ['git', 'branch', '-a'], 'yes': True,
      'help': False, 'version': False}),
    (['thefuck', ARGUMENT_PLACEHOLDER, '-v'],
     {'alias': None, 'command': [], 'yes': False, 'help': False,
      'version': True}),
    (['thefuck', ARGUMENT_PLACEHOLDER, '--help'],
     {'alias': None, 'command': [], 'yes': False, 'help': True,
      'version': False})])
def test_parse(argv, result):
    assert vars(Parser().parse(argv)) == result
