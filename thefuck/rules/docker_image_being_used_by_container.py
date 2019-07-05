from thefuck.utils import for_app


@for_app('docker')
def match(command):
    return ('docker' in command.script
            and 'image is being used by running container' in command.output)


def get_new_command(command):
    container_id = command.output.strip().split(' ')
    print(container_id[-1])
    return 'docker container rm -f {} && {}'.format(container_id[-1], command.script)
