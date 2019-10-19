# -*- encoding: utf-8 -*-
from thefuck.utils import memoize, get_alias

target_layout = '''qwertyuiop[]asdfghjkl;'zxcvbnm,./QWERTYUIOP{}ASDFGHJKL:"ZXCVBNM<>?'''
# any new keyboard layout must be appended

greek = u''';ςερτυθιοπ[]ασδφγηξκλ΄ζχψωβνμ,./:΅ΕΡΤΥΘΙΟΠ{}ΑΣΔΦΓΗΞΚΛ¨"ΖΧΨΩΒΝΜ<>?'''
korean = u'''ㅂㅈㄷㄱㅅㅛㅕㅑㅐㅔ[]ㅁㄴㅇㄹㅎㅗㅓㅏㅣ;'ㅋㅌㅊㅍㅠㅜㅡ,./ㅃㅉㄸㄲㅆㅛㅕㅑㅒㅖ{}ㅁㄴㅇㄹㅎㅗㅓㅏㅣ:"ㅋㅌㅊㅍㅠㅜㅡ<>?'''

source_layouts = [u'''йцукенгшщзхъфывапролджэячсмитьбю.ЙЦУКЕНГШЩЗХЪФЫВАПРОЛДЖЭЯЧСМИТЬБЮ,''',
                  u'''йцукенгшщзхїфівапролджєячсмитьбю.ЙЦУКЕНГШЩЗХЇФІВАПРОЛДЖЄЯЧСМИТЬБЮ,''',
                  u'''ضصثقفغعهخحجچشسیبلاتنمکگظطزرذدپو./ًٌٍَُِّْ][}{ؤئيإأآة»«:؛كٓژٰ‌ٔء><؟''',
                  u'''/'קראטוןםפ][שדגכעיחלךף,זסבהנמצתץ.QWERTYUIOP{}ASDFGHJKL:"ZXCVBNM<>?''',
                  greek,
                  korean]

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

'''Lists used for decomposing korean letters.'''
HEAD_LIST = [u'ㄱ', u'ㄲ', u'ㄴ', u'ㄷ', u'ㄸ', u'ㄹ', u'ㅁ', u'ㅂ', u'ㅃ', u'ㅅ', u'ㅆ',
             u'ㅇ', u'ㅈ', u'ㅉ', u'ㅊ', u'ㅋ', u'ㅌ', u'ㅍ', u'ㅎ']
BODY_LIST = [u'ㅏ', u'ㅐ', u'ㅑ', u'ㅒ', u'ㅓ', u'ㅔ', u'ㅕ', u'ㅖ', u'ㅗ', u'ㅘ', u'ㅙ',
             u'ㅚ', u'ㅛ', u'ㅜ', u'ㅝ', u'ㅞ', u'ㅟ', u'ㅠ', u'ㅡ', u'ㅢ', u'ㅣ']
TAIL_LIST = [u' ', u'ㄱ', u'ㄲ', u'ㄳ', u'ㄴ', u'ㄵ', u'ㄶ', u'ㄷ', u'ㄹ', u'ㄺ', u'ㄻ',
             u'ㄼ', u'ㄽ', u'ㄾ', u'ㄿ', u'ㅀ', u'ㅁ', u'ㅂ', u'ㅄ', u'ㅅ', u'ㅆ', u'ㅇ', u'ㅈ',
             u'ㅊ', u'ㅋ', u'ㅌ', u'ㅍ', u'ㅎ']
DOUBLE_LIST = [u'ㅘ', u'ㅙ', u'ㅚ', u'ㅝ', u'ㅞ', u'ㅟ', u'ㅢ', u'ㄳ', u'ㄵ', u'ㄶ', u'ㄺ',
               u'ㄻ', u'ㄼ', u'ㄽ', u'ㄾ', u'ㅀ', u'ㅄ']
DOUBLE_MOD_LIST = [u'ㅗㅏ', u'ㅗㅐ', u'ㅗㅣ', u'ㅜㅓ', u'ㅜㅔ', u'ㅜㅣ', u'ㅡㅣ', u'ㄱㅅ',
                   u'ㄴㅈ', u'ㄴㅎ', u'ㄹㄱ', u'ㄹㅁ', u'ㄹㅂ', u'ㄹㅅ', u'ㄹㅌ', u'ㄹㅎ', u'ㅂㅅ']


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
        return ch

    hg_str = u''
    for ch in command.script:
        if u'가' <= ch <= u'힣':
            ord_ch = ord(ch) - ord(u'가')
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
    if any(u'ㄱ' <= ch <= u'ㅎ' or u'ㅏ' <= ch <= u'ㅣ' or u'가' <= ch <= u'힣'
            for ch in command.script):
        return True

    matched_layout = _get_matched_layout(command)
    return (matched_layout and
            _switch_command(command, matched_layout) != get_alias())


def get_new_command(command):
    if any(u'ㄱ' <= ch <= u'ㅎ' or u'ㅏ' <= ch <= u'ㅣ' or u'가' <= ch <= u'힣'
            for ch in command.script):
        command.script = _decompose_korean(command)
    matched_layout = _get_matched_layout(command)
    return _switch_command(command, matched_layout)
