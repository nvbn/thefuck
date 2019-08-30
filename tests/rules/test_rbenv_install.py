import pytest
from thefuck.rules.rbenv_install import match, get_new_command
from thefuck.types import Command

expected_actual_command = """cd /home/alex/.rbenv/plugins/ruby-build && git pull && cd -"""
expected_output = """ruby-build: definition not found: 2.6.1

See all available versions with `rbenv install --list'.

If the version you need is missing, try upgrading ruby-build:

  %s""" % expected_actual_command


@pytest.mark.parametrize('script, output', [
    ('rbenv install 2.6.1', expected_output)
])
def test_match(script, output):
    assert match(Command(script, output))


@pytest.mark.parametrize('command, new_command', [
    (Command('rbenv install 2.6.1', expected_output), expected_actual_command)
])
def test_get_new_command(command, new_command):
    assert get_new_command(command) == new_command
