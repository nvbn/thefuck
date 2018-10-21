persian_letters = ('ض', 'ص', 'ث', 'ق', 'ف', 'غ', 'ع', 'ه', 'خ', 'ح', 'ج', 'چ', 'ش', 'س', 'ی', 'ب',
                    'ل', 'ا', 'ت', 'ن', 'م', 'ک', 'گ', 'ظ', 'ط', 'ز', 'ر', 'ذ', 'د', 'پ', 'و')

english_letters = ('q', 'w', 'e', 'r', 't', 'y', 'u', 'i', 'o', 'p', '[', ']', 'a', 's', 'd', 'f',
                    'g', 'h', 'j', 'k', 'l', ';', "'", 'z', 'x', 'c', 'v', 'b', 'n', 'm', ',')

def match(command):
    return (command.script.startswith(persian_letters)
        and 'command not found' in command.output.lower())


def get_new_command(command):
    script = command.script
    for i, letter in enumerate(persian_letters):
        script = script.replace(letter, english_letters[i])
    return script
