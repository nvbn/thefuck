from unittest.mock import patch
import pytest
from subprocess import PIPE
from thefuck.rules.no_command import match, get_new_command
from thefuck.main import Command


@pytest.fixture
def command_found():
    return b'''No command 'aptget' found, did you mean:
 Command 'apt-get' from package 'apt' (main)
aptget: command not found
'''

@pytest.fixture
def command_not_found():
    return b'''No command 'vom' found, but there are 19 similar ones
vom: command not found
'''


def test_match(command_found, command_not_found):
    with patch('thefuck.rules.no_command.Popen') as Popen:
        Popen.return_value.stderr.read.return_value = command_found
        assert match(Command('aptget install vim', '', ''))
        Popen.assert_called_once_with('/usr/lib/command-not-found aptget',
                                      shell=True, stderr=PIPE)
        Popen.return_value.stderr.read.return_value = command_not_found
        assert not match(Command('ls', '', ''))

    with patch('thefuck.rules.no_command.Popen') as Popen:
        Popen.return_value.stderr.read.return_value = command_found
        assert match(Command('sudo aptget install vim', '', ''))
        Popen.assert_called_once_with('/usr/lib/command-not-found aptget',
                                      shell=True, stderr=PIPE)


def test_get_new_command(command_found):
    with patch('thefuck.rules.no_command._get_output',
               return_value=command_found.decode()):
        assert get_new_command(Command('aptget install vim', '', ''))\
            == 'apt-get install vim'
        assert get_new_command(Command('sudo aptget install vim', '', '')) \
            == 'sudo apt-get install vim'
