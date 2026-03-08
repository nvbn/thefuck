def match(command):
    return (
        ('pip install' in command.script or
         'pip3 install' in command.script) and
        'externally-managed-environment' in command.output
    )

def get_new_command(command):
    return command.script + ' --break-system-packages'
