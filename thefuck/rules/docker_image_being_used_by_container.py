from thefuck.utils import for_app
from thefuck.shells import shell


@for_app('docker')
def match(command):
    '''
    Matches a command's output with docker's output
    warning you that you need to remove a container before removing an image.
    '''
    return 'image is being used by running container' in command.output


def get_new_command(command):
    '''
    Prepends docker container rm -f {container ID} to
    the previous docker image rm {image ID} command
    '''
    container_id = command.output.strip().split(' ')
    return shell.and_('docker container rm -f {}', '{}').format(container_id[-1], command.script)
