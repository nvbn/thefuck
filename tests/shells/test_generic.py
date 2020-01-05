# -*- coding: utf-8 -*-

import pytest
from thefuck.shells import Generic


class TestGeneric(object):
    @pytest.fixture
    def shell(self):
        return Generic()

    def test_from_shell(self, shell):
        assert shell.from_shell('pwd') == 'pwd'

    def test_to_shell(self, shell):
        assert shell.to_shell('pwd') == 'pwd'

    def test_and_(self, shell):
        assert shell.and_('ls', 'cd') == 'ls && cd'

    def test_or_(self, shell):
        assert shell.or_('ls', 'cd') == 'ls || cd'

    def test_get_aliases(self, shell):
        assert shell.get_aliases() == {}

    def test_app_alias(self, shell):
        assert 'alias fuck' in shell.app_alias('fuck')
        assert 'alias FUCK' in shell.app_alias('FUCK')
        assert 'thefuck' in shell.app_alias('fuck')
        assert 'TF_ALIAS=fuck PYTHONIOENCODING' in shell.app_alias('fuck')
        assert 'PYTHONIOENCODING=utf-8 thefuck' in shell.app_alias('fuck')

    def test_get_history(self, history_lines, shell):
        history_lines(['ls', 'rm'])
        # We don't know what to do in generic shell with history lines,
        # so just ignore them:
        assert list(shell.get_history()) == []

    def test_split_command(self, shell):
        assert shell.split_command('ls') == ['ls']
        assert shell.split_command(u'echo café') == [u'echo', u'café']

    def test_how_to_configure(self, shell):
        assert shell.how_to_configure() is None

    @pytest.mark.parametrize('side_effect, expected_info, warn', [
        ([u'3.5.9'], u'Generic Shell 3.5.9', False),
        ([OSError], u'Generic Shell', True),
    ])
    def test_info(self, side_effect, expected_info, warn, shell, mocker):
        warn_mock = mocker.patch('thefuck.shells.generic.warn')
        shell._get_version = mocker.Mock(side_effect=side_effect)
        assert shell.info() == expected_info
        assert warn_mock.called is warn
        assert shell._get_version.called
