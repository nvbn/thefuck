# -*- encoding: utf-8 -*-
from thefuck.utils import memoize, get_alias

target_layout = '''qwertyuiop[]asdfghjkl;'zxcvbnm,./QWERTYUIOP{}ASDFGHJKL:"ZXCVBNM<>?'''
# any new keyboard layout must be appended

greek = u''';ςερτυθιοπ[]ασδφγηξκλ΄ζχψωβνμ,./:΅ΕΡΤΥΘΙΟΠ{}ΑΣΔΦΓΗΞΚΛ¨"ΖΧΨΩΒΝΜ<>?'''

source_layouts = [u'''йцукенгшщзхъфывапролджэячсмитьбю.ЙЦУКЕНГШЩЗХЪФЫВАПРОЛДЖЭЯЧСМИТЬБЮ,''',
                  u'''йцукенгшщзхїфівапролджєячсмитьбю.ЙЦУКЕНГШЩЗХЇФІВАПРОЛДЖЄЯЧСМИТЬБЮ,''',
                  u'''ضصثقفغعهخحجچشسیبلاتنمکگظطزرذدپو./ًٌٍَُِّْ][}{ؤئيإأآة»«:؛كٓژٰ‌ٔء><؟''',
                  u'''/'קראטוןםפ][שדגכעיחלךף,זסבהנמצתץ.QWERTYUIOP{}ASDFGHJKL:"ZXCVBNM<>?''',
                  greek]


source_to_target = {
    greek: {u';': "q", u'ς': "w", u'ε': "e", u'ρ': "r", u'τ': "t", u'υ': "y",
            u'θ': "u", u'ι': "i", u'ο': "o", u'π': "p", u'[': "[", u']': "]",
            u'α': "a", u'σ': "s", u'δ': "d", u'φ': "f", u'γ': "g", u'η': "h",
            u'ξ': "j", u'κ': "k", u'λ': "l", u'΄': "'", u'ζ': "z", u'χ': "x",
            u'ψ': "c", u'ω': "v", u'β': "b", u'ν': "n", u'μ': "m", u',': ",",
            u'.': ".", u'/': "/", u':': "Q", u'΅': "W", u'Ε': "E", u'Ρ': "R",
            u'Τ': "T", u'Υ': "Y", u'Θ': "U", u'Ι': "I", u'Ο': "O", u'Π': "P",
            u'{': "{", u'}': "}", u'Α': "A", u'Σ': "S", u'Δ': "D", u'Φ': "F",
            u'Γ': "G", u'Η': "H", u'Ξ': "J", u'Κ': "K", u'Λ': "L", u'¨': ":",
            u'"': '"', u'Ζ': "Z", u'Χ': "X", u'Ψ': "C", u'Ω': "V", u'Β': "B",
            u'Ν': "N", u'Μ': "M", u'<': "<", u'>': ">", u'?': "?", u'ά': "a",
            u'έ': "e", u'ύ': "y", u'ί': "i", u'ό': "o", u'ή': 'h', u'ώ': u"v",
            u'Ά': "A", u'Έ': "E", u'Ύ': "Y", u'Ί': "I", u'Ό': "O", u'Ή': "H",
            u'Ώ': "V"},
}


@memoize
def _get_matched_layout(command):
    # don't use command.split_script here because a layout mismatch will likely
    # result in a non-splitable script as per shlex
    cmd = command.script.split(' ')
    for source_layout in source_layouts:
        is_all_match = True
        for cmd_part in cmd:
            if not all([ch in source_layout or ch in '-_' for ch in cmd_part]):
                is_all_match = False
                break

        if is_all_match:
            return source_layout


def _switch(ch, layout):
    if ch in layout:
        return target_layout[layout.index(ch)]
    else:
        return ch


def _switch_command(command, layout):
    # Layouts with different amount of characters than English
    if layout in source_to_target:
        return ''.join(source_to_target[layout].get(ch, ch)
                       for ch in command.script)

    return ''.join(_switch(ch, layout) for ch in command.script)


def match(command):
    if 'not found' not in command.output:
        return False

    matched_layout = _get_matched_layout(command)
    return (matched_layout and
            _switch_command(command, matched_layout) != get_alias())


def get_new_command(command):
    matched_layout = _get_matched_layout(command)
    return _switch_command(command, matched_layout)
