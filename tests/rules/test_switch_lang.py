# -*- encoding: utf-8 -*-

import pytest
from thefuck.rules import switch_lang
from thefuck.types import Command


@pytest.mark.parametrize('command', [
    Command(u'фзе-пуе', 'command not found: фзе-пуе'),
    Command(u'λσ', 'command not found: λσ'),
    Command(u'שפא-עקא', 'command not found: שפא-עקא'),
    Command(u'ךד', 'command not found: ךד'),
    Command(u'녀애 ㅣㄴ', 'command not found: 녀애 ㅣㄴ')])
def test_match(command):
    assert switch_lang.match(command)


@pytest.mark.parametrize('command', [
    Command(u'pat-get', 'command not found: pat-get'),
    Command(u'ls', 'command not found: ls'),
    Command(u'агсл', 'command not found: агсл'),
    Command(u'фзе-пуе', 'some info'),
    Command(u'שפא-עקא', 'some info'),
    Command(u'녀애 ㅣㄴ', 'some info')])
def test_not_match(command):
    assert not switch_lang.match(command)


@pytest.mark.parametrize('command, new_command', [
    (Command(u'фзе-пуе штыефдд мшь', ''), 'apt-get install vim'),
    (Command(u'λσ -λα', ''), 'ls -la'),
    (Command(u'שפא-עקא ןמדאשךך הןצ', ''), 'apt-get install vim'),
    (Command(u'ךד -ךש', ''), 'ls -la'),
    (Command(u'멧-ㅎㄷㅅ ㅑㅜㄴㅅ미ㅣ 퍄ㅡ', ''), 'apt-get install vim'),
    (Command(u'ㅣㄴ -ㅣㅁ', ''), 'ls- la')])
def test_get_new_command(command, new_command):
    assert switch_lang.get_new_command(command) == new_command
