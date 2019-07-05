from thefuck.utils import for_app, replace_command


@for_app('docker')
def match(command):
    return 'image is being used by running container' in command.output


def get_new_command(command):
    container_id = command.output.split(' ')[-1]
    return 'docker container rm -f {} && {}'.format(container_id, command.script)
