import pytest
from mock import patch
from thefuck.rules import pacman
from thefuck.rules.pacman import match, get_new_command
from tests.utils import Command


pacman_cmd = getattr(pacman, 'pacman', 'pacman')

PKGFILE_OUTPUT_SUDO = 'core/sudo 1.8.13-13/usr/bin/sudo'
PKGFILE_OUTPUT_CONVERT = 'extra/imagemagick 6.9.1.0-1\t/usr/bin/convert'

PKGFILE_OUTPUT_VIM = '''extra/gvim 7.4.712-1        \t/usr/bin/vim
extra/gvim-python3 7.4.712-1\t/usr/bin/vim
extra/vim 7.4.712-1         \t/usr/bin/vim
extra/vim-minimal 7.4.712-1 \t/usr/bin/vim
extra/vim-python3 7.4.712-1 \t/usr/bin/vim'''


@pytest.mark.skipif(not getattr(pacman, 'enabled_by_default', True),
                    reason='Skip if pacman is not available')
@pytest.mark.parametrize('command', [
    Command(script='vim', stderr='vim: command not found'),
    Command(script='sudo vim', stderr='sudo: vim: command not found')])
def test_match(command):
    assert match(command)


@pytest.mark.parametrize('command, return_value', [
    (Command(script='vim', stderr='vim: command not found'), PKGFILE_OUTPUT_VIM),
    (Command(script='sudo vim', stderr='sudo: vim: command not found'), PKGFILE_OUTPUT_VIM)])
@patch('thefuck.specific.archlinux.subprocess')
@patch.multiple(pacman, create=True, pacman=pacman_cmd)
def test_match_mocked(subp_mock, command, return_value):
    subp_mock.check_output.return_value = return_value
    assert match(command)


@pytest.mark.parametrize('command', [
    Command(script='vim', stderr=''), Command(),
    Command(script='sudo vim', stderr=''), Command()])
def test_not_match(command):
    assert not match(command)


sudo_vim_possibilities = ['{} -S extra/gvim && sudo vim',
                          '{} -S extra/gvim-python3 && sudo vim',
                          '{} -S extra/vim && sudo vim',
                          '{} -S extra/vim-minimal && sudo vim',
                          '{} -S extra/vim-python3 && sudo vim']
sudo_vim_possibilities = [s.format(pacman_cmd) for s in sudo_vim_possibilities]

vim_possibilities = ['{} -S extra/gvim && vim',
                     '{} -S extra/gvim-python3 && vim',
                     '{} -S extra/vim && vim',
                     '{} -S extra/vim-minimal && vim',
                     '{} -S extra/vim-python3 && vim']
vim_possibilities = [s.format(pacman_cmd) for s in vim_possibilities]


@pytest.mark.skipif(not getattr(pacman, 'enabled_by_default', True),
                    reason='Skip if pacman is not available')
@pytest.mark.parametrize('command, new_command', [
    (Command('vim'), vim_possibilities),
    (Command('sudo vim'), sudo_vim_possibilities),
    (Command('convert'), ['{} -S extra/imagemagick && convert'.format(pacman_cmd)]),
    (Command('sudo convert'), ['{} -S extra/imagemagick && sudo convert'.format(pacman_cmd)])])
def test_get_new_command(command, new_command, mocker):
    assert get_new_command(command) == new_command


@pytest.mark.parametrize('command, new_command, return_value', [
    (Command('vim'), vim_possibilities, PKGFILE_OUTPUT_VIM),
    (Command('sudo vim'), sudo_vim_possibilities, PKGFILE_OUTPUT_VIM),
    (Command('convert'), ['{} -S extra/imagemagick && convert'.format(pacman_cmd)], PKGFILE_OUTPUT_CONVERT),
    (Command('sudo'), ['{} -S core/sudo && sudo'.format(pacman_cmd)], PKGFILE_OUTPUT_SUDO),
    (Command('sudo convert'), ['{} -S extra/imagemagick && sudo convert'.format(pacman_cmd)], PKGFILE_OUTPUT_CONVERT)])
@patch('thefuck.specific.archlinux.subprocess')
@patch.multiple(pacman, create=True, pacman=pacman_cmd)
def test_get_new_command_mocked(subp_mock, command, new_command, return_value):
    subp_mock.check_output.return_value = return_value
    assert get_new_command(command) == new_command
