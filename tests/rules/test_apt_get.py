import pytest
from mock import Mock, patch
from thefuck.rules import apt_get
from thefuck.rules.apt_get import match, get_new_command
from tests.utils import Command


# python-commandnotfound is available in ubuntu 14.04+
@pytest.mark.skipif(not getattr(apt_get, 'enabled_by_default', True),
                    reason='Skip if python-commandnotfound is not available')
@pytest.mark.parametrize('command', [
    Command(script='vim', stderr='vim: command not found')])
def test_match(command):
    assert match(command)


@pytest.mark.parametrize('command, return_value', [
    (Command(script='vim', stderr='vim: command not found'),
     [('vim', 'main'), ('vim-tiny', 'main')]),
    (Command(script='sudo vim', stderr='vim: command not found'),
     [('vim', 'main'), ('vim-tiny', 'main')])])
@patch('thefuck.rules.apt_get.CommandNotFound', create=True)
@patch.multiple(apt_get, create=True, apt_get='apt_get')
def test_match_mocked(cmdnf_mock, command, return_value):
    get_packages = Mock(return_value=return_value)
    cmdnf_mock.CommandNotFound.return_value = Mock(getPackages=get_packages)
    assert match(command)
    assert cmdnf_mock.CommandNotFound.called
    assert get_packages.called


# python-commandnotfound is available in ubuntu 14.04+
@pytest.mark.skipif(not getattr(apt_get, 'enabled_by_default', True),
                    reason='Skip if python-commandnotfound is not available')
@pytest.mark.parametrize('command', [
    Command(script='a_bad_cmd', stderr='a_bad_cmd: command not found'),
    Command(script='vim', stderr=''), Command()])
def test_not_match(command):
    assert not match(command)


@pytest.mark.parametrize('command, return_value', [
    (Command(script='a_bad_cmd', stderr='a_bad_cmd: command not found'), []),
    (Command(script='vim', stderr=''), []), (Command(), [])])
@patch('thefuck.rules.apt_get.CommandNotFound', create=True)
@patch.multiple(apt_get, create=True, apt_get='apt_get')
def test_not_match_mocked(cmdnf_mock, command, return_value):
    get_packages = Mock(return_value=return_value)
    cmdnf_mock.CommandNotFound.return_value = Mock(getPackages=get_packages)
    assert not match(command)


# python-commandnotfound is available in ubuntu 14.04+
@pytest.mark.skipif(not getattr(apt_get, 'enabled_by_default', True),
                    reason='Skip if python-commandnotfound is not available')
@pytest.mark.parametrize('command, new_command', [
    (Command('vim'), 'sudo apt-get install vim && vim'),
    (Command('convert'), 'sudo apt-get install imagemagick && convert'),
    (Command('sudo vim'), 'sudo apt-get install vim && sudo vim'),
    (Command('sudo convert'), 'sudo apt-get install imagemagick && sudo convert')])
def test_get_new_command(command, new_command):
    assert get_new_command(command) == new_command


@pytest.mark.parametrize('command, new_command, return_value', [
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
@patch('thefuck.rules.apt_get.CommandNotFound', create=True)
@patch.multiple(apt_get, create=True, apt_get='apt_get')
def test_get_new_command_mocked(cmdnf_mock, command, new_command, return_value):
    get_packages = Mock(return_value=return_value)
    cmdnf_mock.CommandNotFound.return_value = Mock(getPackages=get_packages)
    assert get_new_command(command) == new_command
