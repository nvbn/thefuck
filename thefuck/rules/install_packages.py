from thefuck.utils import for_app

@for_app('apt-get') 
def match(command):
    return 'Do you want to continue?' in command.output

def get_new_command(command):
    new_command = command.script.replace('apt-get', 'apt-get -y')
    return new_command