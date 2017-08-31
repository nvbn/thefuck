def match(command):
    return 'manage.py' in command.script and \
           'migrate' in command.script \
           and 'or pass --delete-ghost-migrations' in command.output


def get_new_command(command):
    return u'{} --delete-ghost-migrations'.format(command.script)
