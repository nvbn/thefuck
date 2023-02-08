# -*- encoding: utf-8 -*-

import pytest

from thefuck.rules import switch_lang
from thefuck.types import Command


@pytest.mark.parametrize('command', [
    Command('фзе-пуе', 'command not found: фзе-пуе'),
    Command('λσ', 'command not found: λσ'),
    Command('שפא-עקא', 'command not found: שפא-עקא'),
    Command('ךד', 'command not found: ךד'),
    Command('녀애 ㅣㄴ', 'command not found: 녀애 ㅣㄴ')])
def test_match(command):
    assert switch_lang.match(command)


@pytest.mark.parametrize('command', [
    Command('pat-get', 'command not found: pat-get'),
    Command('ls', 'command not found: ls'),
    Command('агсл', 'command not found: агсл'),
    Command('фзе-пуе', 'some info'),
    Command('שפא-עקא', 'some info'),
    Command('녀애 ㅣㄴ', 'some info')])
def test_not_match(command):
    assert not switch_lang.match(command)


@pytest.mark.parametrize('command, new_command', [
    (Command('фзе-пуе штыефдд мшь', ''), 'apt-get install vim'),
    (Command('λσ -λα', ''), 'ls -la'),
    (Command('שפא-עקא ןמדאשךך הןצ', ''), 'apt-get install vim'),
    (Command('ךד -ךש', ''), 'ls -la'),
    (Command('멧-ㅎㄷㅅ ㅑㅜㄴㅅ미ㅣ 퍄ㅡ', ''), 'apt-get install vim'),
    (Command('ㅣㄴ -ㅣㅁ', ''), 'ls -la'),
    (Command('ㅔㅁㅅ촤', ''), 'patchk'), ])
def test_get_new_command(command, new_command):
    assert switch_lang.get_new_command(command) == new_command
