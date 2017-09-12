# -*- coding: utf-8 -*-

from thefuck.rules.grep_recursive import match, get_new_command
from thefuck.types import Command


def test_match():
    assert match(Command('grep blah .', 'grep: .: Is a directory'))
    assert match(Command(u'grep café .', 'grep: .: Is a directory'))
    assert not match(Command('', ''))


def test_get_new_command():
    assert get_new_command(Command('grep blah .', '')) == 'grep -r blah .'
    assert get_new_command(Command(u'grep café .', '')) == u'grep -r café .'
