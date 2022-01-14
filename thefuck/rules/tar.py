from difflib import SequenceMatcher as SM

patterns = ['tar :', 'exiting now',
            'Cannot open: No such file or directory',
            'Error is not recoverable: exiting now',
            'tar: option requires an argument',
            'option requires an argument',
            'try tar \'--help\' or \'tar --usage\' for more information',
            'try \'tar --help\'', 'try \'tar usage\'',
            'tar: refusing to read archive contents from terminal (missing -f option?)',
            'refusing to read archive contents from terminal', 'error is not recoverable',
            '(missing -f option?)', 'you must specify one of the',
            'you must specify one of the \'-Acdtrux\', \'--delete\' or \'--test-label\' options']

options = ['-cf', '-tvf', '-xf', 'cvf', 'cvzf',
           'cvzfj', '-xvf', '-tvf', '-zvxf', '-jvxf',
           '-zxvf', '-rvf', '-czf', 'tvfW', '-rvf', '-jxvf']

def match(command):
    
    for pattern in patterns:
        if pattern in command.output.lower():
            return True
    return False    

def get_new_command(command):

    # isolate sudo, usually the layout is tar [option] [files -> [input] [output]]     
    # for len                               1      2                 3       4
    # for list                              0       1              2
    com_parts = [part for part in command.script_parts if part != 'sudo']
    
    # see if the percent similarity of the option is greater than 0.5 (50%)
    isolated = [opt for part in command.script_parts for opt in options if SM(None, part.lower(), opt).ratio() > 0.5]
    
    # having a length of more than 2 implies that it is likely that it has an input
    # and output, rather than a trivial mistake
    if len(com_parts) > 2 :     
        return f"{com_parts[0]} {isolated[0]} {' '.join(com_parts[2:len(com_parts)])}"
    else:
        if isolated == []:
            return f"{' '.join([parts for parts in com_parts])}"
        else:
            return f"{com_parts[0]} {isolated[0]}"        
