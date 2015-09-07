# -*- encoding: utf-8 -*-

import pytest
from thefuck.rules import switch_lang
from tests.utils import Command


@pytest.mark.parametrize('command', [
    Command(stderr='command not found: фзе-пуе', script=u'фзе-пуе'),
    Command(stderr='command not found: λσ', script=u'λσ')])
def test_match(command):
    assert switch_lang.match(command)


@pytest.mark.parametrize('command', [
    Command(stderr='command not found: pat-get', script=u'pat-get'),
    Command(stderr='command not found: ls', script=u'ls'),
    Command(stderr='command not found: агсл', script=u'агсл'),
    Command(stderr='some info', script=u'фзе-пуе')])
def test_not_match(command):
    assert not switch_lang.match(command)


@pytest.mark.parametrize('command, new_command', [
    (Command(u'фзе-пуе штыефдд мшь'), 'apt-get install vim'),
    (Command(u'λσ -λα'), 'ls -la')])
def test_get_new_command(command, new_command):
    assert switch_lang.get_new_command(command) == new_command
