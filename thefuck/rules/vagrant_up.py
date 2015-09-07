from thefuck import shells
from thefuck.utils import for_app


@for_app('vagrant')
def match(command):
    return 'run `vagrant up`' in command.stderr.lower()


def get_new_command(command):
    cmds = command.script.split(' ')
    machine = None
    if len(cmds) >= 3:
        machine = cmds[2]

    startAllInstances = shells.and_("vagrant up", command.script)
    if machine is None: 
        return startAllInstances
    else:
        return [ shells.and_("vagrant up " +  machine, command.script), startAllInstances]
