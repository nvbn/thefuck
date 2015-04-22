# -*- encoding: utf-8 -*-

target_layout = '''qwertyuiop[]asdfghjkl;'zxcvbnm,./QWERTYUIOP{}ASDFGHJKL:"ZXCVBNM<>?'''

source_layouts = [u'''йцукенгшщзхъфывапролджэячсмитьбю.ЙЦУКЕНГШЩЗХЪФЫВАПРОЛДЖЭЯЧСМИТЬБЮ,''',
                  u'''ضصثقفغعهخحجچشسیبلاتنمکگظطزرذدپو./ًٌٍَُِّْ][}{ؤئيإأآة»«:؛كٓژٰ‌ٔء><؟''',
                  u''';ςερτυθιοπ[]ασδφγηξκλ΄ζχψωβνμ,./:΅ΕΡΤΥΘΙΟΠ{}ΑΣΔΦΓΗΞΚΛ¨"ΖΧΨΩΒΝΜ<>?''']


def _get_matched_layout(command):
    for source_layout in source_layouts:
        if all([ch in source_layout or ch in '-_'
                for ch in command.script.split(' ')[0]]):
            return source_layout


def match(command, settings):
    return 'not found' in command.stderr and _get_matched_layout(command)


def _switch(ch, layout):
    if ch in layout:
        return target_layout[layout.index(ch)]
    else:
        return ch


def get_new_command(command, settings):
    matched_layout = _get_matched_layout(command)
    return ''.join(_switch(ch, matched_layout) for ch in command.script)

