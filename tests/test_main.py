import pytest
from subprocess import PIPE
from pathlib import PosixPath, Path
from mock import Mock
from thefuck import main, conf, types
from tests.utils import Rule, Command


def test_load_rule(monkeypatch):
    match = object()
    get_new_command = object()
    load_source = Mock()
    load_source.return_value = Mock(match=match,
                                    get_new_command=get_new_command,
                                    enabled_by_default=True)
    monkeypatch.setattr('thefuck.main.load_source', load_source)
    assert main.load_rule(Path('/rules/bash.py')) \
           == Rule('bash', match, get_new_command)
    load_source.assert_called_once_with('bash', '/rules/bash.py')


@pytest.mark.parametrize('conf_rules, rules', [
    (conf.DEFAULT_RULES, [Rule('bash', 'bash', 'bash'),
                          Rule('lisp', 'lisp', 'lisp'),
                          Rule('bash', 'bash', 'bash'),
                          Rule('lisp', 'lisp', 'lisp')]),
    (types.RulesNamesList(['bash']), [Rule('bash', 'bash', 'bash'),
                                      Rule('bash', 'bash', 'bash')])])
def test_get_rules(monkeypatch, conf_rules, rules):
    monkeypatch.setattr(
        'thefuck.main.Path.glob',
        lambda *_: [PosixPath('bash.py'), PosixPath('lisp.py')])
    monkeypatch.setattr('thefuck.main.load_source',
                        lambda x, _: Mock(match=x, get_new_command=x,
                                          enabled_by_default=True))
    assert list(main.get_rules(Path('~'), Mock(rules=conf_rules))) == rules


class TestGetCommand(object):
    @pytest.fixture(autouse=True)
    def Popen(self, monkeypatch):
        Popen = Mock()
        Popen.return_value.stdout.read.return_value = b'stdout'
        Popen.return_value.stderr.read.return_value = b'stderr'
        monkeypatch.setattr('thefuck.main.Popen', Popen)
        return Popen

    @pytest.fixture(autouse=True)
    def prepare(self, monkeypatch):
        monkeypatch.setattr('thefuck.main.os.environ', {})
        monkeypatch.setattr('thefuck.main.wait_output', lambda *_: True)

    @pytest.fixture(autouse=True)
    def generic_shell(self, monkeypatch):
        monkeypatch.setattr('thefuck.shells.from_shell', lambda x: x)
        monkeypatch.setattr('thefuck.shells.to_shell', lambda x: x)

    def test_get_command_calls(self, Popen):
        assert main.get_command(Mock(),
            ['thefuck', 'apt-get', 'search', 'vim']) \
               == Command('apt-get search vim', 'stdout', 'stderr')
        Popen.assert_called_once_with('apt-get search vim',
                                      shell=True,
                                      stdout=PIPE,
                                      stderr=PIPE,
                                      env={'LANG': 'C'})
    @pytest.mark.parametrize('args, result', [
        (['thefuck', 'ls', '-la'], 'ls -la'),
        (['thefuck', 'ls'], 'ls')])
    def test_get_command_script(self, args, result):
        if result:
            assert main.get_command(Mock(), args).script == result
        else:
            assert main.get_command(Mock(), args) is None


class TestGetMatchedRule(object):
    def test_no_match(self):
        assert main.get_matched_rule(
            Command('ls'), [Rule('', lambda *_: False)],
            Mock(no_colors=True)) is None

    def test_match(self):
        rule = Rule('', lambda x, _: x.script == 'cd ..')
        assert main.get_matched_rule(
            Command('cd ..'), [rule], Mock(no_colors=True)) == rule

    def test_when_rule_failed(self, capsys):
        main.get_matched_rule(
            Command('ls'), [Rule('test', Mock(side_effect=OSError('Denied')))],
            Mock(no_colors=True))
        assert capsys.readouterr()[1].split('\n')[0] == '[WARN] Rule test:'


class TestRunRule(object):
    @pytest.fixture(autouse=True)
    def confirm(self, monkeypatch):
        mock = Mock(return_value=True)
        monkeypatch.setattr('thefuck.main.confirm', mock)
        return mock

    def test_run_rule(self, capsys):
        main.run_rule(Rule(get_new_command=lambda *_: 'new-command'),
                      Command(), None)
        assert capsys.readouterr() == ('new-command\n', '')

    def test_run_rule_with_side_effect(self, capsys):
        side_effect = Mock()
        settings = Mock()
        command = Command()
        main.run_rule(Rule(get_new_command=lambda *_: 'new-command',
                           side_effect=side_effect),
                      command, settings)
        assert capsys.readouterr() == ('new-command\n', '')
        side_effect.assert_called_once_with(command, settings)

    def test_when_not_comfirmed(self, capsys, confirm):
        confirm.return_value = False
        main.run_rule(Rule(get_new_command=lambda *_: 'new-command'),
                      Command(), None)
        assert capsys.readouterr() == ('', '')


class TestConfirm(object):
    @pytest.fixture
    def stdin(self, monkeypatch):
        mock = Mock(return_value='\n')
        monkeypatch.setattr('sys.stdin.read', mock)
        return mock

    def test_when_not_required(self, capsys):
        assert main.confirm('command', None, Mock(require_confirmation=False))
        assert capsys.readouterr() == ('', 'command\n')

    def test_with_side_effect_and_without_confirmation(self, capsys):
        assert main.confirm('command', Mock(), Mock(require_confirmation=False))
        assert capsys.readouterr() == ('', 'command*\n')

    # `stdin` fixture should be applied after `capsys`
    def test_when_confirmation_required_and_confirmed(self, capsys, stdin):
        assert main.confirm('command', None, Mock(require_confirmation=True,
                                                  no_colors=True))
        assert capsys.readouterr() == ('', 'command [enter/ctrl+c]')

    # `stdin` fixture should be applied after `capsys`
    def test_when_confirmation_required_and_confirmed_with_side_effect(self, capsys, stdin):
        assert main.confirm('command', Mock(), Mock(require_confirmation=True,
                                                    no_colors=True))
        assert capsys.readouterr() == ('', 'command* [enter/ctrl+c]')

    def test_when_confirmation_required_and_aborted(self, capsys, stdin):
        stdin.side_effect = KeyboardInterrupt
        assert not main.confirm('command', None, Mock(require_confirmation=True,
                                                      no_colors=True))
        assert capsys.readouterr() == ('', 'command [enter/ctrl+c]Aborted\n')
