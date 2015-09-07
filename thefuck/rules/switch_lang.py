# -*- encoding: utf-8 -*-
from thefuck.shells import thefuck_alias
from thefuck.utils import memoize

target_layout = '''qwertyuiop[]asdfghjkl;'zxcvbnm,./QWERTYUIOP{}ASDFGHJKL:"ZXCVBNM<>?'''

source_layouts = [u'''йцукенгшщзхъфывапролджэячсмитьбю.ЙЦУКЕНГШЩЗХЪФЫВАПРОЛДЖЭЯЧСМИТЬБЮ,''',
                  u'''ضصثقفغعهخحجچشسیبلاتنمکگظطزرذدپو./ًٌٍَُِّْ][}{ؤئيإأآة»«:؛كٓژٰ‌ٔء><؟''',
                  u''';ςερτυθιοπ[]ασδφγηξκλ΄ζχψωβνμ,./:΅ΕΡΤΥΘΙΟΠ{}ΑΣΔΦΓΗΞΚΛ¨"ΖΧΨΩΒΝΜ<>?''']


@memoize
def _get_matched_layout(command):
    for source_layout in source_layouts:
        if all([ch in source_layout or ch in '-_'
                for ch in command.script.split(' ')[0]]):
            return source_layout


def _switch(ch, layout):
    if ch in layout:
        return target_layout[layout.index(ch)]
    else:
        return ch


def _switch_command(command, layout):
    return ''.join(_switch(ch, layout) for ch in command.script)


def match(command):
    if 'not found' not in command.stderr:
        return False
    matched_layout = _get_matched_layout(command)
    return matched_layout and \
           _switch_command(command, matched_layout) != thefuck_alias()


def get_new_command(command):
    matched_layout = _get_matched_layout(command)
    return _switch_command(command, matched_layout)
