import pytest
from pathlib import PosixPath, Path
from mock import Mock
from thefuck import corrector, conf, types
from tests.utils import Rule, Command, CorrectedCommand
from thefuck.corrector import make_corrected_commands, get_corrected_commands


def test_load_rule(mocker):
    match = object()
    get_new_command = object()
    load_source = mocker.patch(
        'thefuck.corrector.load_source',
        return_value=Mock(match=match,
                          get_new_command=get_new_command,
                          enabled_by_default=True,
                          priority=900,
                          requires_output=True))
    assert corrector.load_rule(Path('/rules/bash.py')) \
           == Rule('bash', match, get_new_command, priority=900)
    load_source.assert_called_once_with('bash', '/rules/bash.py')


class TestGetRules(object):
    @pytest.fixture
    def glob(self, mocker):
        results = {}
        mocker.patch('pathlib.Path.glob',
                     new_callable=lambda: lambda *_: results.pop('value', []))
        return lambda value: results.update({'value': value})

    @pytest.fixture(autouse=True)
    def load_source(self, monkeypatch):
        monkeypatch.setattr('thefuck.corrector.load_source',
                            lambda x, _: Rule(x))

    def _compare_names(self, rules, names):
        assert {r.name for r in rules} == set(names)

    def _prepare_rules(self, rules):
        if rules == conf.DEFAULT_RULES:
            return rules
        else:
            return types.RulesNamesList(rules)

    @pytest.mark.parametrize('paths, conf_rules, exclude_rules, loaded_rules', [
        (['git.py', 'bash.py'], conf.DEFAULT_RULES, [], ['git', 'bash']),
        (['git.py', 'bash.py'], ['git'], [], ['git']),
        (['git.py', 'bash.py'], conf.DEFAULT_RULES, ['git'], ['bash']),
        (['git.py', 'bash.py'], ['git'], ['git'], [])])
    def test_get_rules(self, glob, settings, paths, conf_rules, exclude_rules,
                       loaded_rules):
        glob([PosixPath(path) for path in paths])
        settings.update(rules=self._prepare_rules(conf_rules),
                        priority={},
                        exclude_rules=self._prepare_rules(exclude_rules))
        rules = corrector.get_rules()
        self._compare_names(rules, loaded_rules)


class TestIsRuleMatch(object):
    def test_no_match(self):
        assert not corrector.is_rule_match(
            Command('ls'), Rule('', lambda _: False))

    def test_match(self):
        rule = Rule('', lambda x: x.script == 'cd ..')
        assert corrector.is_rule_match(Command('cd ..'), rule)

    @pytest.mark.usefixtures('no_colors')
    def test_when_rule_failed(self, capsys):
        rule = Rule('test', Mock(side_effect=OSError('Denied')),
                    requires_output=False)
        assert not corrector.is_rule_match(Command('ls'), rule)
        assert capsys.readouterr()[1].split('\n')[0] == '[WARN] Rule test:'


class TestMakeCorrectedCommands(object):
    def test_with_rule_returns_list(self):
        rule = Rule(get_new_command=lambda x: [x.script + '!', x.script + '@'],
                    priority=100)
        assert list(make_corrected_commands(Command(script='test'), rule)) \
               == [CorrectedCommand(script='test!', priority=100),
                   CorrectedCommand(script='test@', priority=200)]

    def test_with_rule_returns_command(self):
        rule = Rule(get_new_command=lambda x: x.script + '!',
                    priority=100)
        assert list(make_corrected_commands(Command(script='test'), rule)) \
               == [CorrectedCommand(script='test!', priority=100)]

def test_get_corrected_commands(mocker):
    command = Command('test', 'test', 'test')
    rules = [Rule(match=lambda _: False),
             Rule(match=lambda _: True,
                  get_new_command=lambda x: x.script + '!', priority=100),
             Rule(match=lambda _: True,
                  get_new_command=lambda x: [x.script + '@', x.script + ';'],
                  priority=60)]
    mocker.patch('thefuck.corrector.get_rules', return_value=rules)
    assert [cmd.script for cmd in get_corrected_commands(command)] \
           == ['test!', 'test@', 'test;']
