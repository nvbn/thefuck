# -*- encoding: utf-8 -*-
from thefuck.utils import memoize, get_alias

target_layout = '''qwertyuiop[]asdfghjkl;'zxcvbnm,./QWERTYUIOP{}ASDFGHJKL:"ZXCVBNM<>?'''
#any new keyboard layout must be appended

source_layouts = [u'''йцукенгшщзхъфывапролджэячсмитьбю.ЙЦУКЕНГШЩЗХЪФЫВАПРОЛДЖЭЯЧСМИТЬБЮ,''',
                  u'''йцукенгшщзхїфівапролджєячсмитьбю.ЙЦУКЕНГШЩЗХЇФІВАПРОЛДЖЄЯЧСМИТЬБЮ,''',
                  u'''ضصثقفغعهخحجچشسیبلاتنمکگظطزرذدپو./ًٌٍَُِّْ][}{ؤئيإأآة»«:؛كٓژٰ‌ٔء><؟''',
                  u''';ςερτυθιοπ[]ασδφγηξκλ΄ζχψωβνμ,./:΅ΕΡΤΥΘΙΟΠ{}ΑΣΔΦΓΗΞΚΛ¨"ΖΧΨΩΒΝΜ<>?''',
                  u'''/'קראטוןםפ][שדגכעיחלךף,זסבהנמצתץ.QWERTYUIOP{}ASDFGHJKL:"ZXCVBNM<>?''']


@memoize
def _get_matched_layout(command):
    # don't use command.split_script here because a layout mismatch will likely
    # result in a non-splitable sript as per shlex
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
    if (source_layouts.index(layout) == 3):# this is for the Greek keyboard
        keyboardDic = {';': "q", 'ς': "w", 'ε': "e", 'ρ': "r", 'τ': "t", 'υ': "y", 'θ': "u", 'ι': "i", 'ο': "o", 'π': "p",
                       '[': "[", ']': "]", 'α': "a", 'σ': "s", 'δ': "d", 'φ': "f", 'γ': "g", 'η': "h", 'ξ': "j", 'κ': "k",
                       'λ': "l", ';': ";", '΄': "'", 'ζ': "z", 'χ': "x", 'ψ': "c", 'ω': "v", 'β': "b", 'ν': "n", 'μ': "m", 
                       ',': ",", '.': ".", '/': "/", ':': "Q", '΅': "W", 'Ε': "E", 'Ρ': "R", 'Τ': "T", 'Υ': "Y", 'Θ': "U",
                       'Ι': "I", 'Ο': "O", 'Π': "P", '{': "{", '}': "}", 'Α': "A", 'Σ': "S", 'Δ': "D", 'Φ': "F", 'Γ': "G",
                       'Η': "H", 'Ξ': "J", 'Κ': "K", 'Λ': "L", '¨': ":", '"': '"', 'Ζ': "Z", 'Χ': "X", 'Ψ': "C", 'Ω': "V",
                       'Β': "B", 'Ν': "N", 'Μ': "M", '<': "<", '>': ">", '?': "?", 'ά': "a", 'έ': "e", 'ύ': "y", 'ί': "i",
                       'ό': "o", 'ή': 'h', 'ώ': "v", 'Ά': "A", 'Έ': "E", 'Ύ': "Y", 'Ί': "I", 'Ό': "O", 'Ή': "H", 'Ώ': "V"}
        newCommand = ""
        for ch in command.script:
            try:
                newCommand += keyboardDic[ch]
            except KeyError:# This character has no repressentation at the dictionary, so it is a symbol and therefore we can add him, now works only for spaces and for this symbol "-"
                newCommand += ch
   
        return(newCommand)

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
