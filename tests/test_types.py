from mock import Mock
from pathlib import Path
import pytest
from tests.utils import CorrectedCommand, Rule, Command
from thefuck import conf


class TestCorrectedCommand(object):

    def test_equality(self):
        assert CorrectedCommand('ls', None, 100) == \
               CorrectedCommand('ls', None, 200)
        assert CorrectedCommand('ls', None, 100) != \
               CorrectedCommand('ls', lambda *_: _, 100)

    def test_hashable(self):
        assert {CorrectedCommand('ls', None, 100),
                CorrectedCommand('ls', None, 200)} == {CorrectedCommand('ls')}


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
        assert Rule.from_path(Path('/rules/bash.py')) \
               == Rule('bash', match, get_new_command, priority=900)
        load_source.assert_called_once_with('bash', '/rules/bash.py')

    @pytest.mark.parametrize('rules, exclude_rules, rule, is_enabled', [
        (conf.DEFAULT_RULES, [], Rule('git', enabled_by_default=True), True),
        (conf.DEFAULT_RULES, [], Rule('git', enabled_by_default=False), False),
        ([], [], Rule('git', enabled_by_default=False), False),
        ([], [], Rule('git', enabled_by_default=True), False),
        (conf.DEFAULT_RULES + ['git'], [], Rule('git', enabled_by_default=False), True),
        (['git'], [], Rule('git', enabled_by_default=False), True),
        (conf.DEFAULT_RULES, ['git'], Rule('git', enabled_by_default=True), False),
        (conf.DEFAULT_RULES, ['git'], Rule('git', enabled_by_default=False), False),
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
