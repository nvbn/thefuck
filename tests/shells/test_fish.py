# -*- coding: utf-8 -*-

import pytest
from thefuck.shells import Fish


@pytest.mark.usefixtures('isfile', 'no_memoize', 'no_cache')
class TestFish(object):
    @pytest.fixture
    def shell(self):
        return Fish()

    @pytest.fixture(autouse=True)
    def Popen(self, mocker):
        mock = mocker.patch('thefuck.shells.fish.Popen')
        mock.return_value.stdout.read.return_value = (
            b'cd\nfish_config\nfuck\nfunced\nfuncsave\ngrep\nhistory\nll\nls\n'
            b'man\nmath\npopd\npushd\nruby')
        return mock

    @pytest.fixture
    def environ(self, monkeypatch):
        data = {'TF_OVERRIDDEN_ALIASES': 'cd, ls, man, open'}
        monkeypatch.setattr('thefuck.shells.fish.os.environ', data)
        return data

    @pytest.mark.usefixture('environ')
    def test_get_overridden_aliases(self, shell, environ):
        assert shell._get_overridden_aliases() == ['cd', 'ls', 'man', 'open']

    @pytest.mark.parametrize('before, after', [
        ('cd', 'cd'),
        ('pwd', 'pwd'),
        ('fuck', 'fish -ic "fuck"'),
        ('find', 'find'),
        ('funced', 'fish -ic "funced"'),
        ('grep', 'grep'),
        ('awk', 'awk'),
        ('math "2 + 2"', r'fish -ic "math \"2 + 2\""'),
        ('man', 'man'),
        ('open', 'open'),
        ('vim', 'vim'),
        ('ll', 'fish -ic "ll"'),
        ('ls', 'ls')])  # Fish has no aliases but functions
    def test_from_shell(self, before, after, shell):
        assert shell.from_shell(before) == after

    def test_to_shell(self, shell):
        assert shell.to_shell('pwd') == 'pwd'

    def test_and_(self, shell):
        assert shell.and_('foo', 'bar') == 'foo; and bar'

    def test_get_aliases(self, shell):
        assert shell.get_aliases() == {'fish_config': 'fish_config',
                                       'fuck': 'fuck',
                                       'funced': 'funced',
                                       'funcsave': 'funcsave',
                                       'history': 'history',
                                       'll': 'll',
                                       'math': 'math',
                                       'popd': 'popd',
                                       'pushd': 'pushd',
                                       'ruby': 'ruby'}

    def test_app_alias(self, shell):
        assert 'function fuck' in shell.app_alias('fuck')
        assert 'function FUCK' in shell.app_alias('FUCK')
        assert 'thefuck' in shell.app_alias('fuck')
        assert 'TF_ALIAS=fuck PYTHONIOENCODING' in shell.app_alias('fuck')
        assert 'PYTHONIOENCODING=utf-8 thefuck' in shell.app_alias('fuck')

    def test_get_history(self, history_lines, shell):
        history_lines(['- cmd: ls', '  when: 1432613911',
                       '- cmd: rm', '  when: 1432613916'])
        assert list(shell.get_history()) == ['ls', 'rm']
