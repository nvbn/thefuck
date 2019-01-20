# -*- encoding: utf-8 -*-
from thefuck.utils import memoize, get_alias

target_layout = '''qwertyuiop[]asdfghjkl;'zxcvbnm,./QWERTYUIOP{}ASDFGHJKL:"ZXCVBNM<>?'''
# any new keyboard layout must be appended

greek = u''';ςερτυθιοπ[]ασδφγηξκλ΄ζχψωβνμ,./:΅ΕΡΤΥΘΙΟΠ{}ΑΣΔΦΓΗΞΚΛ¨"ΖΧΨΩΒΝΜ<>?'''

source_layouts = [u'''йцукенгшщзхъфывапролджэячсмитьбю.ЙЦУКЕНГШЩЗХЪФЫВАПРОЛДЖЭЯЧСМИТЬБЮ,''',
                  u'''йцукенгшщзхїфівапролджєячсмитьбю.ЙЦУКЕНГШЩЗХЇФІВАПРОЛДЖЄЯЧСМИТЬБЮ,''',
                  u'''ضصثقفغعهخحجچشسیبلاتنمکگظطزرذدپو./ًٌٍَُِّْ][}{ؤئيإأآة»«:؛كٓژٰ‌ٔء><؟''',
                  u'''/'קראטוןםפ][שדגכעיחלךף,זסבהנמצתץ.QWERTYUIOP{}ASDFGHJKL:"ZXCVBNM<>?''',
                  u'''ㅂㅈㄷㄱㅅㅛㅕㅑㅐㅔ[]ㅁㄴㅇㄹㅎㅗㅓㅏㅣ;'ㅋㅌㅊㅍㅠㅜㅡ,./ㅃㅉㄸㄲㅆㅛㅕㅑㅒㅖ{}ㅁㄴㅇㄹㅎㅗㅓㅏㅣ:"ㅋㅌㅊㅍㅠㅜㅡ<>?''',
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

'''Lists used for decomposing korean letters'''
HEAD_LIST = ['ㄱ', 'ㄲ', 'ㄴ', 'ㄷ', 'ㄸ', 'ㄹ', 'ㅁ', 'ㅂ', 'ㅃ', 'ㅅ', 'ㅆ',
             'ㅇ', 'ㅈ', 'ㅉ', 'ㅊ', 'ㅋ', 'ㅌ', 'ㅍ', 'ㅎ']
BODY_LIST = ['ㅏ', 'ㅐ', 'ㅑ', 'ㅒ', 'ㅓ', 'ㅔ', 'ㅕ', 'ㅖ', 'ㅗ', 'ㅘ', 'ㅙ',
             'ㅚ', 'ㅛ', 'ㅜ', 'ㅝ', 'ㅞ', 'ㅟ', 'ㅠ', 'ㅡ', 'ㅢ', 'ㅣ']
TAIL_LIST = [' ', 'ㄱ', 'ㄲ', 'ㄳ', 'ㄴ', 'ㄵ', 'ㄶ', 'ㄷ', 'ㄹ', 'ㄺ', 'ㄻ',
             'ㄼ', 'ㄽ', 'ㄾ', 'ㄿ', 'ㅀ', 'ㅁ', 'ㅂ', 'ㅄ', 'ㅅ', 'ㅆ', 'ㅇ', 'ㅈ',
             'ㅊ', 'ㅋ', 'ㅌ', 'ㅍ', 'ㅎ']
DOUBLE_LIST = ['ㅘ', 'ㅙ', 'ㅚ', 'ㅝ', 'ㅞ', 'ㅟ', 'ㅢ', 'ㄳ', 'ㄵ', 'ㄶ', 'ㄺ',
               'ㄻ', 'ㄼ', 'ㄽ', 'ㄾ', 'ㅀ', 'ㅄ']
DOUBLE_MOD_LIST = ['ㅗㅏ', 'ㅗㅐ', 'ㅗㅣ', 'ㅜㅓ', 'ㅜㅔ', 'ㅜㅣ', 'ㅡㅣ', 'ㄱㅅ',
                   'ㄴㅈ', 'ㄴㅎ', 'ㄹㄱ', 'ㄹㅁ', 'ㄹㅂ', 'ㄹㅅ', 'ㄹㅌ', 'ㄹㅎ', 'ㅂㅅ']


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


def _decompose_korean(command):
    def _change_double(ch):
        if ch in DOUBLE_LIST:
            return DOUBLE_MOD_LIST[DOUBLE_LIST.index(ch)]
        else:
            return ch

    hg_str = ''
    for ch in command.script:
        if '가' <= ch <= '힣':
            ord_ch = ord(ch) - ord('가')
            hd = ord_ch // 588
            bd = (ord_ch - 588 * hd) // 28
            tl = ord_ch - 588 * hd - 28 * bd
            for ch in [HEAD_LIST[hd], BODY_LIST[bd], TAIL_LIST[tl]]:
                if ch != ' ':
                    hg_str += _change_double(ch)
        else:
            hg_str += _change_double(ch)
    return hg_str


def match(command):
    if 'not found' not in command.output:
        return False
    if any(['ㄱ' <= ch <= 'ㅎ' or 'ㅏ' <= ch <= 'ㅣ' or '가' <= ch <= '힣'
            for ch in command.script]):
        command.script = _decompose_korean(command)

    matched_layout = _get_matched_layout(command)
    return (matched_layout and
            _switch_command(command, matched_layout) != get_alias())


def get_new_command(command):
    matched_layout = _get_matched_layout(command)
    return _switch_command(command, matched_layout)
