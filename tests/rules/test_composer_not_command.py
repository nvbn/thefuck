import pytest
from thefuck.rules.composer_not_command import match, get_new_command
from thefuck.types import Command

# tested with composer version 1.9.0

# command: composer udpate
case_single_command_with_one_suggestion = ("composer udpate", r'\n'
                                           '                                                                  ''\n'
                                           r'  [Symfony\Component\Console\Exception\CommandNotFoundException]  ''\n'
                                           '  Command "udpate" is not defined.                                ''\n'
                                           '                                                                  ''\n'
                                           '  Did you mean this?                                              ''\n'
                                           '      update                                                      ''\n'
                                           '                                                                  ''\n'
                                           '\n'
                                           )
case_single_command_with_one_suggestion_expected = "composer update"

# command: composer selupdate
case_single_command_with_many_suggestions = ("composer selupdate", r'\n'
                                             '                                                                  ''\n'
                                             r'  [Symfony\Component\Console\Exception\CommandNotFoundException]  ''\n'
                                             '  Command "selupdate" is not defined.                             ''\n'
                                             '                                                                  ''\n'
                                             '  Did you mean one of these?                                      ''\n'
                                             '      update                                                      ''\n'
                                             '      self-update                                                 ''\n'
                                             '      selfupdate                                                  ''\n'
                                             '                                                                  ''\n'
                                             '\n'
                                             )
case_single_command_with_many_suggesitons_expected = ["composer update", "composer self-update", "composer selfupdate"]


@pytest.mark.parametrize('command', [Command(*v) for v in [
    case_single_command_with_one_suggestion,
    case_single_command_with_many_suggestions
]])
def test_match(command):
    assert match(command)


@pytest.mark.parametrize('command, new_command', [(Command(*t[0]), t[1]) for t in [
    (case_single_command_with_one_suggestion, case_single_command_with_one_suggestion_expected),
    (case_single_command_with_many_suggestions, case_single_command_with_many_suggesitons_expected)
]])
def test_get_new_command(command, new_command):
    assert get_new_command(command) == new_command
