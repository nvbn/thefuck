# -*- coding: utf-8 -*-

import pytest
from thefuck.rules.remove_trailing_cedilla import match, get_new_command
from tests.utils import Command

@pytest.mark.parametrize('command', [
    Command(script='wrongç'),
    Command(script='wrong with argsç')])

def test_match(command):
    assert match(command)

@pytest.mark.parametrize('command, new_command', [
    (Command('wrongç'), 'wrong'),
    (Command('wrong with argsç'), 'wrong with args')])
def test_get_new_command(command, new_command):
    assert get_new_command(command) == new_command
