import pytest

from thefuck.rules.tar_missed_arguments import match, get_new_command
from thefuck.types import Command


@pytest.mark.parametrize(
    "script, output",
    [
        ("tar tarname.tar /workspaces/", "tar: invalid option -- '.'"),

        ("tar tar_name.tar",
         "Try 'tar --help' or 'tar --usage' for more information."),

        ("tar name_tar.tar /workspaces/thefuck/rules",
         "tar: invalid option -- '.'\nTry 'tar --help' or 'tar --usage' for more information."),
    ],
)
def test_match(script, output):
    assert match(Command(script, output))


@pytest.mark.parametrize(
    "script, output",
    [
        ("python release.py", ""),

        ("tar tarname.tar /workspaces/", ""),

        ("tar -cvf tar_name.tar", "tar: Cowardly refusing to create an empty archive"),

        ("tar -cvfj /workspaces/thefuck",
         "Try 'tar --help' or 'tar --usage' for more information."),

        ("tar -cvzf /workspaces/thefuck/rules",
         "tar: invalid option -- '.'\nTry 'tar --help' or 'tar --usage' for more information."),

        ("tar -jxvf tar_name.tar", "tar: Cowardly refusing to create an empty archive"),

        ("tar -xvf /workspaces/thefuck",
         "Try 'tar --help' or 'tar --usage' for more information."),

        ("tar -zxvf /workspaces/thefuck/rules",
         "tar: invalid option -- '.'\nTry 'tar --help' or 'tar --usage' for more information."),
    ],
)
def test_not_match(script, output):
    assert not match(Command(script, output))


@pytest.mark.parametrize(
    "script, output, new_command",
    [
        ("tar tar_name.tar /workspaces",
         "tar: You may not specify more than one '-Acdtrux', '--delete' or  '--test-label' option",
         [
             "tar -cvf tar_name.tar /workspaces", "tar -cvfj tar_name.tar /workspaces",
             "tar -cvzf tar_name.tar /workspaces", "tar -jxvf tar_name.tar /workspaces",
             "tar -xvf tar_name.tar /workspaces", "tar -zxvf tar_name.tar /workspaces"
         ]),

        ("tar tar_name.tar /workspaces/thefuck",
         "Try 'tar --help' or 'tar --usage' for more information.",
         [
             "tar -cvf tar_name.tar /workspaces/thefuck",
             "tar -cvfj tar_name.tar /workspaces/thefuck",
             "tar -cvzf tar_name.tar /workspaces/thefuck",
             "tar -jxvf tar_name.tar /workspaces/thefuck",
             "tar -xvf tar_name.tar /workspaces/thefuck",
             "tar -zxvf tar_name.tar /workspaces/thefuck"
         ]),

        ("tar tar_name.tar /workspaces/thefuck/rules",
         "tar: invalid option -- '.'\nTry 'tar --help' or 'tar --usage' for more information.",
         [
             "tar -cvf tar_name.tar /workspaces/thefuck/rules",
             "tar -cvfj tar_name.tar /workspaces/thefuck/rules",
             "tar -cvzf tar_name.tar /workspaces/thefuck/rules",
             "tar -jxvf tar_name.tar /workspaces/thefuck/rules",
             "tar -xvf tar_name.tar /workspaces/thefuck/rules",
             "tar -zxvf tar_name.tar /workspaces/thefuck/rules"
         ]),
    ],
)
def test_get_new_command(script, output, new_command):
    assert get_new_command(Command(script, output)) == new_command
