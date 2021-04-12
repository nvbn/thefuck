import pytest
from thefuck.rules.rvm_use import match, get_new_command
from thefuck.types import Command


output = pattern = """RVM is not a function, selecting rubies with 'rvm use ...' will not work.

You need to change your terminal emulator preferences to allow login shell.
Sometimes it is required to use `/bin/bash --login` as the command.
Please visit https://rvm.io/integration/gnome-terminal/ for an example."""


@pytest.mark.parametrize('command', [
    Command('rvm use 2.7.2', output),
    Command('rvm use 3.0.1', output),
    Command('rvm use 1.6.7', output)])
def test_match(command):
    assert match(command)


@pytest.mark.parametrize('command, new_command', [
    (Command('rvm use 2.7.2', output), 'rvm install "ruby-2.7.2"; rvm use 2.7.2'),
    (Command('rvm use 3.0.1', output), 'rvm install "ruby-3.0.1"; rvm use 3.0.1'),
    (Command('rvm use 1.6.7', output), 'rvm install "ruby-1.6.7"; rvm use 1.6.7')])
def test_get_new_command(command, new_command):
    assert get_new_command(command) == new_command
