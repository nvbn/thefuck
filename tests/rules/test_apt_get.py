import pytest
from thefuck.rules.apt_get import match, get_new_command
from tests.utils import Command


@pytest.mark.parametrize('command, packages', [
    (Command(script='vim', stderr='vim: command not found'),
     [('vim', 'main'), ('vim-tiny', 'main')]),
    (Command(script='sudo vim', stderr='vim: command not found'),
     [('vim', 'main'), ('vim-tiny', 'main')]),
    (Command(script='vim', stderr="The program 'vim' is currently not installed. You can install it by typing: sudo apt install vim"),
     [('vim', 'main'), ('vim-tiny', 'main')])])
def test_match(mocker, command, packages):
    mocker.patch('thefuck.rules.apt_get.which', return_value=None)
    mock = mocker.patch('thefuck.rules.apt_get.command_not_found',
                        create=True)
    mock.getPackages.return_value = packages

    assert match(command)


@pytest.mark.parametrize('command, packages, which', [
    (Command(script='a_bad_cmd', stderr='a_bad_cmd: command not found'),
     [], None),
    (Command(script='vim', stderr=''), [], None),
    (Command(), [], None),
    (Command(script='vim', stderr='vim: command not found'),
     ['vim'], '/usr/bin/vim'),
    (Command(script='sudo vim', stderr='vim: command not found'),
     ['vim'], '/usr/bin/vim')])
def test_not_match(mocker, command, packages, which):
    mocker.patch('thefuck.rules.apt_get.which', return_value=which)
    mock = mocker.patch('thefuck.rules.apt_get.command_not_found',
                        create=True)
    mock.getPackages.return_value = packages

    assert not match(command)


@pytest.mark.parametrize('command, new_command, packages', [
    (Command('vim'), 'sudo apt-get install vim && vim',
     [('vim', 'main'), ('vim-tiny', 'main')]),
    (Command('convert'), 'sudo apt-get install imagemagick && convert',
     [('imagemagick', 'main'),
      ('graphicsmagick-imagemagick-compat', 'universe')]),
    (Command('sudo vim'), 'sudo apt-get install vim && sudo vim',
     [('vim', 'main'), ('vim-tiny', 'main')]),
    (Command('sudo convert'), 'sudo apt-get install imagemagick && sudo convert',
     [('imagemagick', 'main'),
      ('graphicsmagick-imagemagick-compat', 'universe')])])
def test_get_new_command(mocker, command, new_command, packages):
    mock = mocker.patch('thefuck.rules.apt_get.command_not_found',
                        create=True)
    mock.getPackages.return_value = packages
    assert get_new_command(command) == new_command
