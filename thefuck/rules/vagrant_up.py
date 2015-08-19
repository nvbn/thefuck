from thefuck import shells


def match(command, settings):
    return command.script.startswith('vagrant ') and 'run `vagrant up`' in command.stderr.lower()

def get_new_command(command, settings):
    cmds = command.script.split(' ')
    machine = ""
    if len(cmds) >= 3:
        machine = cmds[2]
    return "vagrant up " +  machine + " && " + command.script
