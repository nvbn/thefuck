# -*- encoding: utf-8 -*-

from thefuck.rules.fix_alt_space import match, get_new_command
from thefuck.types import Command


def test_match():
    """The character before 'grep' is Alt+Space, which happens frequently
    on the Mac when typing the pipe character (Alt+7), and holding the Alt
    key pressed for longer than necessary.

    """
    assert match(Command(u'ps -ef | grep foo',
                         u'-bash:  grep: command not found'))
    assert not match(Command('ps -ef | grep foo', ''))
    assert not match(Command('', ''))


def test_get_new_command():
    """ Replace the Alt+Space character by a simple space """
    assert (get_new_command(Command(u'ps -ef | grep foo', ''))
            == 'ps -ef | grep foo')
