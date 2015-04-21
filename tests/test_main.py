from subprocess import PIPE
from pathlib import PosixPath, Path
from mock import patch, Mock
from thefuck import main


def test_get_settings():
    with patch('thefuck.main.load_source', return_value=Mock(rules=['bash'])):
        assert main.get_settings(Path('/')).rules == ['bash']
    with patch('thefuck.main.load_source', return_value=Mock(spec=[])):
        assert main.get_settings(Path('/')).rules is None


def test_is_rule_enabled():
    assert main.is_rule_enabled(Mock(rules=None), Path('bash.py'))
    assert main.is_rule_enabled(Mock(rules=['bash']), Path('bash.py'))
    assert not main.is_rule_enabled(Mock(rules=['bash']), Path('lisp.py'))


def test_load_rule():
    match = object()
    get_new_command = object()
    with patch('thefuck.main.load_source',
               return_value=Mock(
                   match=match,
                   get_new_command=get_new_command)) as load_source:
        assert main.load_rule(Path('/rules/bash.py')) == main.Rule(match, get_new_command)
        load_source.assert_called_once_with('bash', '/rules/bash.py')


def test_get_rules():
    with patch('thefuck.main.Path.glob') as glob, \
            patch('thefuck.main.load_source',
                  lambda x, _: Mock(match=x, get_new_command=x)):
        glob.return_value = [PosixPath('bash.py'), PosixPath('lisp.py')]
        assert main.get_rules(
            Path('~'),
            Mock(rules=None)) == [main.Rule('bash', 'bash'),
                                  main.Rule('lisp', 'lisp'),
                                  main.Rule('bash', 'bash'),
                                  main.Rule('lisp', 'lisp')]
        assert main.get_rules(
            Path('~'),
            Mock(rules=['bash'])) == [main.Rule('bash', 'bash'),
                                      main.Rule('bash', 'bash')]


def test_get_command():
    with patch('thefuck.main.Popen') as Popen, \
            patch('thefuck.main.os.environ',
                  new_callable=lambda: {}), \
            patch('thefuck.main.wait_output',
                  return_value=True):
        Popen.return_value.stdout.read.return_value = b'stdout'
        Popen.return_value.stderr.read.return_value = b'stderr'
        assert main.get_command(Mock(), [b'thefuck', b'apt-get',
                                         b'search', b'vim']) \
               == main.Command('apt-get search vim', 'stdout', 'stderr')
        Popen.assert_called_once_with('apt-get search vim',
                                      shell=True,
                                      stdout=PIPE,
                                      stderr=PIPE,
                                      env={'LANG': 'C'})


def test_get_matched_rule():
    rules = [main.Rule(lambda x, _: x.script == 'cd ..', None),
             main.Rule(lambda *_: False, None)]
    assert main.get_matched_rule(main.Command('ls', '', ''),
                                 rules, None) is None
    assert main.get_matched_rule(main.Command('cd ..', '', ''),
                                 rules, None) == rules[0]


def test_run_rule(capsys):
    with patch('thefuck.main.confirm', return_value=True):
        main.run_rule(main.Rule(None, lambda *_: 'new-command'),
                      None, None)
        assert capsys.readouterr() == ('new-command\n', '')
    with patch('thefuck.main.confirm', return_value=False):
        main.run_rule(main.Rule(None, lambda *_: 'new-command'),
                      None, None)
        assert capsys.readouterr() == ('', '')


def test_confirm(capsys):
    # When confirmation not required:
    assert main.confirm('command', Mock(require_confirmation=False))
    assert capsys.readouterr() == ('', 'command\n')
    # When confirmation required and confirmed:
    with patch('thefuck.main.sys.stdin.read', return_value='\n'):
        assert main.confirm('command', Mock(require_confirmation=True))
        assert capsys.readouterr() == ('', 'command [Enter/Ctrl+C]')
    # When confirmation required and ctrl+c:
    with patch('thefuck.main.sys.stdin.read', side_effect=KeyboardInterrupt):
        assert not main.confirm('command', Mock(require_confirmation=True))
        assert capsys.readouterr() == ('', 'command [Enter/Ctrl+C]Aborted\n')
