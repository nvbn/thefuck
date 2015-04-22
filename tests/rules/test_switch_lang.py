# -*- encoding: utf-8 -*-

from mock import Mock
from thefuck.rules import switch_lang


def test_match():
    assert switch_lang.match(Mock(stderr='command not found: фзе-пуе',
                                  script=u'фзе-пуе'), None)
    assert switch_lang.match(Mock(stderr='command not found: λσ',
                                  script=u'λσ'), None)

    assert not switch_lang.match(Mock(stderr='command not found: pat-get',
                                      script=u'pat-get'), None)
    assert not switch_lang.match(Mock(stderr='command not found: ls',
                                      script=u'ls'), None)
    assert not switch_lang.match(Mock(stderr='some info',
                                      script=u'фзе-пуе'), None)


def test_get_new_command():
    assert switch_lang.get_new_command(
        Mock(script=u'фзе-пуе штыефдд мшь'), None) == 'apt-get install vim'
    assert switch_lang.get_new_command(
        Mock(script=u'λσ -λα'), None) == 'ls -la'
