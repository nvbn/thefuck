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
    assert corrector.load_rule(Path('/rules/bash.py'), settings=Mock(priority={})) \
           == Rule('bash', match, get_new_command, priority=900)
    load_source.assert_called_once_with('bash', '/rules/bash.py')


class TestGetRules(object):
    @pytest.fixture(autouse=True)
    def glob(self, mocker):
        return mocker.patch('thefuck.corrector.Path.glob', return_value=[])

    def _compare_names(self, rules, names):
        return [r.name for r in rules] == names

    @pytest.mark.parametrize('conf_rules, rules', [
        (conf.DEFAULT_RULES, ['bash', 'lisp', 'bash', 'lisp']),
        (types.RulesNamesList(['bash']), ['bash', 'bash'])])
    def test_get(self, monkeypatch, glob, conf_rules, rules):
        glob.return_value = [PosixPath('bash.py'), PosixPath('lisp.py')]
        monkeypatch.setattr('thefuck.corrector.load_source',
                            lambda x, _: Rule(x))
        assert self._compare_names(
            corrector.get_rules(Path('~'), Mock(rules=conf_rules, priority={})),
            rules)


class TestGetMatchedRules(object):
    def test_no_match(self):
        assert list(corrector.get_matched_rules(
            Command('ls'), [Rule('', lambda *_: False)],
            Mock(no_colors=True))) == []

    def test_match(self):
        rule = Rule('', lambda x, _: x.script == 'cd ..')
        assert list(corrector.get_matched_rules(
            Command('cd ..'), [rule], Mock(no_colors=True))) == [rule]

    def test_when_rule_failed(self, capsys):
        all(corrector.get_matched_rules(
            Command('ls'), [Rule('test', Mock(side_effect=OSError('Denied')),
                                 requires_output=False)],
            Mock(no_colors=True, debug=False)))
        assert capsys.readouterr()[1].split('\n')[0] == '[WARN] Rule test:'


class TestGetCorrectedCommands(object):
    def test_with_rule_returns_list(self):
        rule = Rule(get_new_command=lambda x, _: [x.script + '!', x.script + '@'],
                    priority=100)
        assert list(make_corrected_commands(Command(script='test'), [rule], None)) \
               == [CorrectedCommand(script='test!', priority=100),
                   CorrectedCommand(script='test@', priority=200)]

    def test_with_rule_returns_command(self):
        rule = Rule(get_new_command=lambda x, _: x.script + '!',
                    priority=100)
        assert list(make_corrected_commands(Command(script='test'), [rule], None)) \
               == [CorrectedCommand(script='test!', priority=100)]


def test_get_corrected_commands(mocker):
    command = Command('test', 'test', 'test')
    rules = [Rule(match=lambda *_: False),
             Rule(match=lambda *_: True,
                  get_new_command=lambda x, _: x.script + '!', priority=100),
             Rule(match=lambda *_: True,
                  get_new_command=lambda x, _: [x.script + '@', x.script + ';'],
                  priority=60)]
    mocker.patch('thefuck.corrector.get_rules', return_value=rules)
    assert [cmd.script for cmd in get_corrected_commands(command, None, Mock(debug=False))] \
           == ['test!', 'test@', 'test;']
