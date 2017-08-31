from thefuck.shells import shell
from thefuck.utils import for_app


@for_app('vagrant')
def match(command):
    return 'run `vagrant up`' in command.output.lower()


def get_new_command(command):
    cmds = command.script_parts
    machine = None
    if len(cmds) >= 3:
        machine = cmds[2]

    start_all_instances = shell.and_(u"vagrant up", command.script)
    if machine is None:
        return start_all_instances
    else:
        return [shell.and_(u"vagrant up {}".format(machine), command.script),
                start_all_instances]
