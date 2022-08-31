# -*- coding: utf-8 -*-

import pytest
from theheck.const import ARGUMENT_PLACEHOLDER
from theheck.shells import Fish


@pytest.mark.usefixtures('isfile', 'no_memoize', 'no_cache')
class TestFish(object):
    @pytest.fixture
    def shell(self):
        return Fish()

    @pytest.fixture(autouse=True)
    def Popen(self, mocker):
        mock = mocker.patch('theheck.shells.fish.Popen')
        mock.return_value.stdout.read.side_effect = [(
            b'cd\nfish_config\nheck\nfunced\nfuncsave\ngrep\nhistory\nll\nls\n'
            b'man\nmath\npopd\npushd\nruby'),
            (b'alias fish_key_reader /usr/bin/fish_key_reader\nalias g git\n'
             b'alias alias_with_equal_sign=echo\ninvalid_alias'), b'func1\nfunc2', b'']
        return mock

    @pytest.mark.parametrize('key, value', [
        ('TF_OVERRIDDEN_ALIASES', 'cut,git,sed'),  # legacy
        ('THEHECK_OVERRIDDEN_ALIASES', 'cut,git,sed'),
        ('THEHECK_OVERRIDDEN_ALIASES', 'cut, git, sed'),
        ('THEHECK_OVERRIDDEN_ALIASES', ' cut,\tgit,sed\n'),
        ('THEHECK_OVERRIDDEN_ALIASES', '\ncut,\n\ngit,\tsed\r')])
    def test_get_overridden_aliases(self, shell, os_environ, key, value):
        os_environ[key] = value
        overridden = shell._get_overridden_aliases()
        assert set(overridden) == {'cd', 'cut', 'git', 'grep',
                                   'ls', 'man', 'open', 'sed'}

    @pytest.mark.parametrize('before, after', [
        ('cd', 'cd'),
        ('pwd', 'pwd'),
        ('heck', 'fish -ic "heck"'),
        ('find', 'find'),
        ('funced', 'fish -ic "funced"'),
        ('grep', 'grep'),
        ('awk', 'awk'),
        ('math "2 + 2"', r'fish -ic "math \"2 + 2\""'),
        ('man', 'man'),
        ('open', 'open'),
        ('vim', 'vim'),
        ('ll', 'fish -ic "ll"'),
        ('ls', 'ls'),
        ('g', 'git')])
    def test_from_shell(self, before, after, shell):
        assert shell.from_shell(before) == after

    def test_to_shell(self, shell):
        assert shell.to_shell('pwd') == 'pwd'

    def test_and_(self, shell):
        assert shell.and_('foo', 'bar') == 'foo; and bar'

    def test_or_(self, shell):
        assert shell.or_('foo', 'bar') == 'foo; or bar'

    def test_get_aliases(self, shell):
        assert shell.get_aliases() == {'fish_config': 'fish_config',
                                       'heck': 'heck',
                                       'funced': 'funced',
                                       'funcsave': 'funcsave',
                                       'history': 'history',
                                       'll': 'll',
                                       'math': 'math',
                                       'popd': 'popd',
                                       'pushd': 'pushd',
                                       'ruby': 'ruby',
                                       'g': 'git',
                                       'fish_key_reader': '/usr/bin/fish_key_reader',
                                       'alias_with_equal_sign': 'echo'}
        assert shell.get_aliases() == {'func1': 'func1', 'func2': 'func2'}

    def test_app_alias(self, shell):
        assert 'function heck' in shell.app_alias('heck')
        assert 'function HECK' in shell.app_alias('HECK')
        assert 'theheck' in shell.app_alias('heck')
        assert 'TF_SHELL=fish' in shell.app_alias('heck')
        assert 'TF_ALIAS=heck PYTHONIOENCODING' in shell.app_alias('heck')
        assert 'PYTHONIOENCODING=utf-8 theheck' in shell.app_alias('heck')
        assert ARGUMENT_PLACEHOLDER in shell.app_alias('heck')

    def test_app_alias_alter_history(self, settings, shell):
        settings.alter_history = True
        assert (
            'builtin history delete --exact --case-sensitive -- $hecked_up_command\n'
            in shell.app_alias('HECK')
        )
        assert 'builtin history merge\n' in shell.app_alias('HECK')
        settings.alter_history = False
        assert 'builtin history delete' not in shell.app_alias('HECK')
        assert 'builtin history merge' not in shell.app_alias('HECK')

    def test_get_history(self, history_lines, shell):
        history_lines(['- cmd: ls', '  when: 1432613911',
                       '- cmd: rm', '  when: 1432613916'])
        assert list(shell.get_history()) == ['ls', 'rm']

    @pytest.mark.parametrize('entry, entry_utf8', [
        ('ls', '- cmd: ls\n   when: 1430707243\n'),
        (u'echo café', '- cmd: echo café\n   when: 1430707243\n')])
    def test_put_to_history(self, entry, entry_utf8, builtins_open, mocker, shell):
        mocker.patch('theheck.shells.fish.time', return_value=1430707243.3517463)
        shell.put_to_history(entry)
        builtins_open.return_value.__enter__.return_value. \
            write.assert_called_once_with(entry_utf8)

    def test_how_to_configure(self, shell, config_exists):
        config_exists.return_value = True
        assert shell.how_to_configure().can_configure_automatically

    def test_how_to_configure_when_config_not_found(self, shell,
                                                    config_exists):
        config_exists.return_value = False
        assert not shell.how_to_configure().can_configure_automatically

    def test_get_version(self, shell, Popen):
        Popen.return_value.stdout.read.side_effect = [b'fish, version 3.5.9\n']
        assert shell._get_version() == '3.5.9'
        assert Popen.call_args[0][0] == ['fish', '--version']

    @pytest.mark.parametrize('side_effect, exception', [
        ([b'\n'], IndexError),
        (OSError('file not found'), OSError),
    ])
    def test_get_version_error(self, side_effect, exception, shell, Popen):
        Popen.return_value.stdout.read.side_effect = side_effect
        with pytest.raises(exception):
            shell._get_version()
        assert Popen.call_args[0][0] == ['fish', '--version']
