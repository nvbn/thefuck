# Code not tested

def match(command, settings):
    return command.script == 'rm -rf /'
    
def get_new_command(command, settings):
    return 'print(\'lol\')'
