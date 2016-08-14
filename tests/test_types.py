# -*- coding: utf-8 -*-

import os
from subprocess import PIPE
from mock import Mock
import pytest
from tests.utils import CorrectedCommand, Rule, Command
from thefuck import const
from thefuck.exceptions import EmptyCommand
from thefuck.system import Path


class TestCorrectedCommand(object):

    def test_equality(self):
        assert CorrectedCommand('ls', None, 100) == \
               CorrectedCommand('ls', None, 200)
        assert CorrectedCommand('ls', None, 100) != \
               CorrectedCommand('ls', lambda *_: _, 100)

    def test_hashable(self):
        assert {CorrectedCommand('ls', None, 100),
                CorrectedCommand('ls', None, 200)} == {CorrectedCommand('ls')}

    def test_representable(self):
        assert '{}'.format(CorrectedCommand('ls', None, 100)) == \
               'CorrectedCommand(script=ls, side_effect=None, priority=100)'
        assert u'{}'.format(CorrectedCommand(u'echo café', None, 100)) == \
               u'CorrectedCommand(script=echo café, side_effect=None, priority=100)'


class TestRule(object):
    def test_from_path(self, mocker):
        match = object()
        get_new_command = object()
        load_source = mocker.patch(
            'thefuck.types.load_source',
            return_value=Mock(match=match,
                              get_new_command=get_new_command,
                              enabled_by_default=True,
                              priority=900,
                              requires_output=True))
        rule_path = os.path.join(os.sep, 'rules', 'bash.py')
        assert Rule.from_path(Path(rule_path)) \
               == Rule('bash', match, get_new_command, priority=900)
        load_source.assert_called_once_with('bash', rule_path)

    @pytest.mark.parametrize('rules, exclude_rules, rule, is_enabled', [
        (const.DEFAULT_RULES, [], Rule('git', enabled_by_default=True), True),
        (const.DEFAULT_RULES, [], Rule('git', enabled_by_default=False), False),
        ([], [], Rule('git', enabled_by_default=False), False),
        ([], [], Rule('git', enabled_by_default=True), False),
        (const.DEFAULT_RULES + ['git'], [], Rule('git', enabled_by_default=False), True),
        (['git'], [], Rule('git', enabled_by_default=False), True),
        (const.DEFAULT_RULES, ['git'], Rule('git', enabled_by_default=True), False),
        (const.DEFAULT_RULES, ['git'], Rule('git', enabled_by_default=False), False),
        ([], ['git'], Rule('git', enabled_by_default=True), False),
        ([], ['git'], Rule('git', enabled_by_default=False), False)])
    def test_is_enabled(self, settings, rules, exclude_rules, rule, is_enabled):
        settings.update(rules=rules,
                        exclude_rules=exclude_rules)
        assert rule.is_enabled == is_enabled

    def test_isnt_match(self):
        assert not Rule('', lambda _: False).is_match(
            Command('ls'))

    def test_is_match(self):
        rule = Rule('', lambda x: x.script == 'cd ..')
        assert rule.is_match(Command('cd ..'))

    @pytest.mark.usefixtures('no_colors')
    def test_isnt_match_when_rule_failed(self, capsys):
        rule = Rule('test', Mock(side_effect=OSError('Denied')),
                    requires_output=False)
        assert not rule.is_match(Command('ls'))
        assert capsys.readouterr()[1].split('\n')[0] == '[WARN] Rule test:'

    def test_get_corrected_commands_with_rule_returns_list(self):
        rule = Rule(get_new_command=lambda x: [x.script + '!', x.script + '@'],
                    priority=100)
        assert list(rule.get_corrected_commands(Command(script='test'))) \
               == [CorrectedCommand(script='test!', priority=100),
                   CorrectedCommand(script='test@', priority=200)]

    def test_get_corrected_commands_with_rule_returns_command(self):
        rule = Rule(get_new_command=lambda x: x.script + '!',
                    priority=100)
        assert list(rule.get_corrected_commands(Command(script='test'))) \
               == [CorrectedCommand(script='test!', priority=100)]


class TestCommand(object):
    @pytest.fixture(autouse=True)
    def Popen(self, monkeypatch):
        Popen = Mock()
        Popen.return_value.stdout.read.return_value = b'stdout'
        Popen.return_value.stderr.read.return_value = b'stderr'
        monkeypatch.setattr('thefuck.types.Popen', Popen)
        return Popen

    @pytest.fixture(autouse=True)
    def prepare(self, monkeypatch):
        monkeypatch.setattr('thefuck.types.os.environ', {})
        monkeypatch.setattr('thefuck.types.Command._wait_output',
                            staticmethod(lambda *_: True))

    def test_from_script_calls(self, Popen, settings):
        settings.env = {}
        assert Command.from_raw_script(
            ['apt-get', 'search', 'vim']) == Command(
            'apt-get search vim', 'stdout', 'stderr')
        Popen.assert_called_once_with('apt-get search vim',
                                      shell=True,
                                      stdin=PIPE,
                                      stdout=PIPE,
                                      stderr=PIPE,
                                      env={})

    @pytest.mark.parametrize('script, result', [
        ([''], None),
        (['', ''], None),
        (['ls', '-la'], 'ls -la'),
        (['ls'], 'ls')])
    def test_from_script(self, script, result):
        if result:
            assert Command.from_raw_script(script).script == result
        else:
            with pytest.raises(EmptyCommand):
                Command.from_raw_script(script)
