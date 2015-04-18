from subprocess import PIPE
from mock import patch, Mock
import pytest
from thefuck.rules.no_command import match, get_new_command
from thefuck.main import Command


@pytest.fixture
def command_found():
    return b'''No command 'aptget' found, did you mean:
 Command 'apt-get' from package 'apt' (main)
 Command 'not-installed' from package 'derp' (main)
 Command 'not-really-used' from package 'whatever' (main)
aptget: command not found
'''

@pytest.fixture
def uninstalled_command_found():
    return b'''No command 'pish' found, did you mean:
 Command 'vish' from package 'vish' (universe)
 Command 'wish' from package 'tk' (main)
 Command 'fish' from package 'fish' (universe)
 Command 'pdsh' from package 'pdsh' (universe)
pish: command not found
'''

@pytest.fixture
def command_not_found():
    return b'''No command 'vom' found, but there are 19 similar ones
vom: command not found
'''

@pytest.fixture
def bins_exists(request):
    p = patch('thefuck.rules.no_command.which',
              return_value=True)
    p.start()
    request.addfinalizer(p.stop)

@pytest.fixture
def bin_might_exist(request):
    def side_effect(name):
        return name in ['not-really-used', 'apt-get', '/usr/lib/command-not-found', 'test']
    p = patch('thefuck.rules.no_command.which',
              side_effect = side_effect)
    p.start()
    request.addfinalizer(p.stop)
            

@pytest.fixture
def patch_history(request):
    def side_effect(name):
        print("history('{}')".format(name))
        count = 2 if name == 'not-really-used' else 12
    p = patch('thefuck.rules.no_command._count_history_uses',
              side_effect = side_effect)
    p.start()
    request.addfinalizer(p.stop)
    


@pytest.fixture
def settings():
    class _Settings(object):
        pass
    return _Settings


@pytest.mark.usefixtures('bin_might_exist', 'patch_history')
def test_match(command_found, command_not_found, uninstalled_command_found, settings):
    with patch('thefuck.rules.no_command.Popen') as Popen:
        Popen.return_value.stderr.read.return_value = command_found
        assert match(Command('aptget install vim', '', ''), settings)
        Popen.assert_called_with('/usr/lib/command-not-found aptget',
                                      shell=True, stderr=PIPE)
        Popen.return_value.stderr.read.return_value = command_not_found
        assert not match(Command('ls', '', ''), settings)

    with patch('thefuck.rules.no_command.Popen') as Popen:
        Popen.return_value.stderr.read.return_value = command_found
        assert match(Command('sudo aptget install vim', '', ''),
                     Mock(command_not_found='test'))
        Popen.assert_called_with('test aptget',
                                      shell=True, stderr=PIPE)

    with patch('thefuck.rules.no_command.Popen') as Popen:
        Popen.return_value.stderr.read.return_value = uninstalled_command_found
        assert not match(Command('pish bla blah', '', ''), settings)

@pytest.mark.usefixtures('bin_might_exist', 'patch_history')
def test_get_new_command(command_found):
    with patch('thefuck.rules.no_command._get_output',
               return_value=command_found.decode()):
        assert get_new_command(Command('aptget install vim', '', ''), settings)\
            == 'apt-get install vim'
        assert get_new_command(Command('sudo aptget install vim', '', ''), settings) \
            == 'sudo apt-get install vim'
