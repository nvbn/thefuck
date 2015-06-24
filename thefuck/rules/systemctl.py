"""
The confusion in systemctl's param order is massive
"""
from thefuck.utils import sudo_support

@sudo_support
def match(command, settings):
    #Catches 'Unknown operation 'service'.' when executing systemctl with misordered arguments
    cmd = command.script.split()
    return ('systemctl' in command.script) and ('Unknown operation \'' in command.stderr) and (len(cmd) - cmd.index('systemctl') == 3);

@sudo_support
def get_new_command(command, settings):
    cmd = command.script.split()
    cmd[len(cmd)-1], cmd[len(cmd)-2] = cmd[len(cmd)-2], cmd[len(cmd)-1]
    return ' '.join(cmd)
