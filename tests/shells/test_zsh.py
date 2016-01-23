# -*- coding: utf-8 -*-

import pytest
from thefuck.shells.zsh import Zsh


@pytest.mark.usefixtures('isfile')
class TestZsh(object):
    @pytest.fixture
    def shell(self):
        return Zsh()

    @pytest.fixture(autouse=True)
    def Popen(self, mocker):
        mock = mocker.patch('thefuck.shells.zsh.Popen')
        mock.return_value.stdout.read.return_value = (
            b'fuck=\'eval $(thefuck $(fc -ln -1 | tail -n 1))\'\n'
            b'l=\'ls -CF\'\n'
            b'la=\'ls -A\'\n'
            b'll=\'ls -alF\'')
        return mock

    @pytest.mark.parametrize('before, after', [
        ('fuck', 'eval $(thefuck $(fc -ln -1 | tail -n 1))'),
        ('pwd', 'pwd'),
        ('ll', 'ls -alF')])
    def test_from_shell(self, before, after, shell):
        assert shell.from_shell(before) == after

    def test_to_shell(self, shell):
        assert shell.to_shell('pwd') == 'pwd'

    @pytest.mark.parametrize('entry, entry_utf8', [
        ('ls', ': 1430707243:0;ls\n'),
        (u'echo café', ': 1430707243:0;echo café\n')])
    def test_put_to_history(self, entry, entry_utf8, builtins_open, mocker, shell):
        mocker.patch('thefuck.shells.zsh.time',
                     return_value=1430707243.3517463)
        shell.put_to_history(entry)
        builtins_open.return_value.__enter__.return_value. \
            write.assert_called_once_with(entry_utf8)

    def test_and_(self, shell):
        assert shell.and_('ls', 'cd') == 'ls && cd'

    def test_get_aliases(self, shell):
        assert shell.get_aliases() == {
            'fuck': 'eval $(thefuck $(fc -ln -1 | tail -n 1))',
            'l': 'ls -CF',
            'la': 'ls -A',
            'll': 'ls -alF'}

    def test_app_alias(self, shell):
        assert 'alias fuck' in shell.app_alias('fuck')
        assert 'alias FUCK' in shell.app_alias('FUCK')
        assert 'thefuck' in shell.app_alias('fuck')
        assert 'TF_ALIAS=fuck PYTHONIOENCODING' in shell.app_alias('fuck')
        assert 'PYTHONIOENCODING=utf-8 thefuck' in shell.app_alias('fuck')

    def test_get_history(self, history_lines, shell):
        history_lines([': 1432613911:0;ls', ': 1432613916:0;rm'])
        assert list(shell.get_history()) == ['ls', 'rm']
