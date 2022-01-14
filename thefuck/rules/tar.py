from difflib import SequenceMatcher as SM

patterns = ['tar :', 'exiting now',
            'Cannot open: No such file or directory',
            'Error is not recoverable: exiting now',
            'tar: option requires an argument',
            'option requires an argument',
            'Try tar \'--help\' or \'tar --usage\' for more information',
            'try \'tar --help\'', 'try \'tar usage\'']

options = ['-cf', '-tvf', '-xf', 'cvf', 'cvzf',
           'cvzfj', '-xvf', '-tvf', '-zvxf', '-jvxf',
           '-zxvf', '-rvf']

def match(command):
    
    for pattern in patterns:
        if pattern in command.output.lower():
            return True
    return False    

def get_new_command(command):
    
    com_parts = [part for part in command.script_parts if part != 'sudo']
    isolated = sorted([opt for part in command.script_parts for opt in options if SM(None, part.lower(), opt).ratio() > 0.5])
    
    if len(com_parts) > 2 :     
        return f"{com_parts[0]} {isolated[0]} {' '.join(com_parts[2:len(com_parts)])}"
    else:
        return f"{com_parts[0]} {isolated[0]}"
            
