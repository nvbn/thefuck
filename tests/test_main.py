from subprocess import PIPE
from pathlib import PosixPath, Path
from mock import patch, Mock
from thefuck import main


def test_setup_user_dir():
    with patch('thefuck.main.Path.is_dir', return_value=False), \
         patch('thefuck.main.Path.mkdir') as mkdir, \
            patch('thefuck.main.Path.touch') as touch:
        main.setup_user_dir()
        assert mkdir.call_count == 2
        assert touch.call_count == 1
    with patch('thefuck.main.Path.is_dir', return_value=True), \
         patch('thefuck.main.Path.mkdir') as mkdir, \
            patch('thefuck.main.Path.touch') as touch:
        main.setup_user_dir()
        assert mkdir.call_count == 0
        assert touch.call_count == 0


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
    with patch('thefuck.main.Popen') as Popen:
        Popen.return_value.stdout.read.return_value = b'stdout'
        Popen.return_value.stderr.read.return_value = b'stderr'
        assert main.get_command(['thefuck', 'apt-get', 'search', 'vim']) \
               == main.Command('apt-get search vim', 'stdout', 'stderr')
        Popen.assert_called_once_with('apt-get search vim',
                                      shell=True,
                                      stdout=PIPE,
                                      stderr=PIPE)


def test_get_matched_rule():
    rules = [main.Rule(lambda x, _: x.script == 'cd ..', None),
             main.Rule(lambda *_: False, None)]
    assert main.get_matched_rule(main.Command('ls', '', ''),
                                 rules, None) is None
    assert main.get_matched_rule(main.Command('cd ..', '', ''),
                                 rules, None) == rules[0]
