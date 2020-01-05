# -*- coding: utf-8 -*-

import os
import pytest
from thefuck.shells import Bash


@pytest.mark.usefixtures('isfile', 'no_memoize', 'no_cache')
class TestBash(object):
    @pytest.fixture
    def shell(self):
        return Bash()

    @pytest.fixture(autouse=True)
    def Popen(self, mocker):
        mock = mocker.patch('thefuck.shells.bash.Popen')
        return mock

    @pytest.fixture(autouse=True)
    def shell_aliases(self):
        os.environ['TF_SHELL_ALIASES'] = (
            'alias fuck=\'eval $(thefuck $(fc -ln -1))\'\n'
            'alias l=\'ls -CF\'\n'
            'alias la=\'ls -A\'\n'
            'alias ll=\'ls -alF\'')

    @pytest.mark.parametrize('before, after', [
        ('pwd', 'pwd'),
        ('fuck', 'eval $(thefuck $(fc -ln -1))'),
        ('awk', 'awk'),
        ('ll', 'ls -alF')])
    def test_from_shell(self, before, after, shell):
        assert shell.from_shell(before) == after

    def test_to_shell(self, shell):
        assert shell.to_shell('pwd') == 'pwd'

    def test_and_(self, shell):
        assert shell.and_('ls', 'cd') == 'ls && cd'

    def test_or_(self, shell):
        assert shell.or_('ls', 'cd') == 'ls || cd'

    def test_get_aliases(self, shell):
        assert shell.get_aliases() == {'fuck': 'eval $(thefuck $(fc -ln -1))',
                                       'l': 'ls -CF',
                                       'la': 'ls -A',
                                       'll': 'ls -alF'}

    def test_app_alias(self, shell):
        assert 'fuck () {' in shell.app_alias('fuck')
        assert 'FUCK () {' in shell.app_alias('FUCK')
        assert 'thefuck' in shell.app_alias('fuck')
        assert 'PYTHONIOENCODING' in shell.app_alias('fuck')

    def test_app_alias_variables_correctly_set(self, shell):
        alias = shell.app_alias('fuck')
        assert "fuck () {" in alias
        assert 'TF_SHELL=bash' in alias
        assert "TF_ALIAS=fuck" in alias
        assert 'PYTHONIOENCODING=utf-8' in alias
        assert 'TF_SHELL_ALIASES=$(alias)' in alias

    def test_get_history(self, history_lines, shell):
        history_lines(['ls', 'rm'])
        assert list(shell.get_history()) == ['ls', 'rm']

    def test_split_command(self, shell):
        command = 'git log -p'
        command_parts = ['git', 'log', '-p']
        assert shell.split_command(command) == command_parts

    def test_how_to_configure(self, shell, config_exists):
        config_exists.return_value = True
        assert shell.how_to_configure().can_configure_automatically

    def test_how_to_configure_when_config_not_found(self, shell,
                                                    config_exists):
        config_exists.return_value = False
        assert not shell.how_to_configure().can_configure_automatically

    def test_info(self, shell, Popen):
        Popen.return_value.stdout.read.side_effect = [b'3.5.9']
        assert shell.info() == 'Bash 3.5.9'

    def test_get_version_error(self, shell, Popen):
        Popen.return_value.stdout.read.side_effect = OSError
        with pytest.raises(OSError):
            shell._get_version()
        assert Popen.call_args[0][0] == ['bash', '-c', 'echo $BASH_VERSION']
