from thefuck.shells import shell
from thefuck.utils import for_app
from thefuck.specific.sudo import sudo_support


@for_app("docker")
def match(command):
    return ('Cannot connect to the Docker daemon' in command.output and
            'Is the docker daemon running?' in command.output)


@sudo_support
def get_new_command(command):
    cmd = command.script_parts[0]
    return shell.and_('systemctl start {}'.format(cmd),
                      command.script)
