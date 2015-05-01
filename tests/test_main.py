from subprocess import PIPE
from pathlib import PosixPath, Path
from mock import patch, Mock
from thefuck import main, conf, types
from tests.utils import Rule, Command


def test_load_rule():
    match = object()
    get_new_command = object()
    with patch('thefuck.main.load_source',
               return_value=Mock(
                   match=match,
                   get_new_command=get_new_command,
                   enabled_by_default=True)) as load_source:
        assert main.load_rule(Path('/rules/bash.py')) \
               == Rule('bash', match, get_new_command)
        load_source.assert_called_once_with('bash', '/rules/bash.py')


def test_get_rules():
    with patch('thefuck.main.Path.glob') as glob, \
            patch('thefuck.main.load_source',
                  lambda x, _: Mock(match=x, get_new_command=x,
                                    enabled_by_default=True)):
        glob.return_value = [PosixPath('bash.py'), PosixPath('lisp.py')]
        assert list(main.get_rules(
            Path('~'),
            Mock(rules=conf.DEFAULT_RULES))) \
               == [Rule('bash', 'bash', 'bash'),
                   Rule('lisp', 'lisp', 'lisp'),
                   Rule('bash', 'bash', 'bash'),
                   Rule('lisp', 'lisp', 'lisp')]
        assert list(main.get_rules(
            Path('~'),
            Mock(rules=types.RulesNamesList(['bash'])))) \
               == [Rule('bash', 'bash', 'bash'),
                   Rule('bash', 'bash', 'bash')]


def test_get_command():
    with patch('thefuck.main.Popen') as Popen, \
            patch('thefuck.main.os.environ',
                  new_callable=lambda: {}), \
            patch('thefuck.main.wait_output',
                  return_value=True):
        Popen.return_value.stdout.read.return_value = b'stdout'
        Popen.return_value.stderr.read.return_value = b'stderr'
        assert main.get_command(Mock(), Mock(),
            ['thefuck', 'apt-get', 'search', 'vim']) \
               == Command('apt-get search vim', 'stdout', 'stderr')
        Popen.assert_called_once_with('apt-get search vim',
                                      shell=True,
                                      stdout=PIPE,
                                      stderr=PIPE,
                                      env={'LANG': 'C'})
        assert main.get_command(Mock(), Mock(), ['']) is None
        # When command is `fuck`:
        assert main.get_command(
            Mock(),
            Mock(last_script='ls', last_fixed_script='ls -la'),
            ['thefuck', 'fuck']).script == 'ls -la'
        # When command equals to last command:
        assert main.get_command(
            Mock(),
            Mock(last_script='ls', last_fixed_script='ls -la'),
            ['thefuck', 'ls']).script == 'ls -la'
        # When last command is `fuck` and no last fixed script:
        assert main.get_command(
            Mock(),
            Mock(last_script='ls', last_fixed_script=''),
            ['thefuck', 'ls']).script == 'ls'


def test_get_matched_rule(capsys):
    rules = [Rule('', lambda x, _: x.script == 'cd ..'),
             Rule('', lambda *_: False),
             Rule('rule', Mock(side_effect=OSError('Denied')))]
    assert main.get_matched_rule(Command('ls'),
                                 rules, Mock(no_colors=True)) is None
    assert main.get_matched_rule(Command('cd ..'),
                                 rules, Mock(no_colors=True)) == rules[0]
    assert capsys.readouterr()[1].split('\n')[0] \
           == '[WARN] Rule rule:'


def test_run_rule(capsys):
    with patch('thefuck.main.confirm', return_value=True):
        main.run_rule(Rule(get_new_command=lambda *_: 'new-command'),
                      Command(), Mock(), None)
        assert capsys.readouterr() == ('new-command\n', '')
        # With side effect:
        side_effect = Mock()
        settings = Mock()
        command = Mock(script='ls')
        history = Mock()
        main.run_rule(Rule(get_new_command=lambda *_: 'new-command',
                           side_effect=side_effect),
                      command, history, settings)
        assert capsys.readouterr() == ('new-command\n', '')
        side_effect.assert_called_once_with(command, settings)
        # Ensure that history updated:
        history.update.assert_called_once_with(last_script='ls',
                                               last_fixed_script='new-command')
    with patch('thefuck.main.confirm', return_value=False):
        main.run_rule(Rule(get_new_command=lambda *_: 'new-command'),
                      Command(), Mock(), None)
        assert capsys.readouterr() == ('', '')


def test_confirm(capsys):
    # When confirmation not required:
    assert main.confirm('command', None, Mock(require_confirmation=False))
    assert capsys.readouterr() == ('', 'command\n')
    # With side effect and without confirmation:
    assert main.confirm('command', Mock(), Mock(require_confirmation=False))
    assert capsys.readouterr() == ('', 'command*\n')
    # When confirmation required and confirmed:
    with patch('thefuck.main.sys.stdin.read', return_value='\n'):
        assert main.confirm(
            'command', None, Mock(require_confirmation=True,
                                  no_colors=True))
        assert capsys.readouterr() == ('', 'command [enter/ctrl+c]')
        # With side effect:
        assert main.confirm(
            'command', Mock(), Mock(require_confirmation=True,
                                    no_colors=True))
        assert capsys.readouterr() == ('', 'command* [enter/ctrl+c]')
    # When confirmation required and ctrl+c:
    with patch('thefuck.main.sys.stdin.read', side_effect=KeyboardInterrupt):
        assert not main.confirm('command', None,
                                Mock(require_confirmation=True,
                                     no_colors=True))
        assert capsys.readouterr() == ('', 'command [enter/ctrl+c]Aborted\n')
