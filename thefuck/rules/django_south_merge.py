def match(command):
    return 'manage.py' in command.script and \
           'migrate' in command.script \
           and '--merge: will just attempt the migration' in command.stderr


def get_new_command(command):
    return u'{} --merge'.format(command.script)
