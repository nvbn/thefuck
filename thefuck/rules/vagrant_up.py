from thefuck import shells


def match(command, settings):
    return command.script.startswith('vagrant ') and 'run `vagrant up`' in command.stderr.lower()


def get_new_command(command, settings):
    cmds = command.script.split(' ')
    machine = None
    if len(cmds) >= 3:
        machine = cmds[2]

    startAllInstances = shells.and_("vagrant up", command.script)
    if machine is None: 
        return startAllInstances
    else:
        return [ shells.and_("vagrant up " +  machine, command.script), startAllInstances]
