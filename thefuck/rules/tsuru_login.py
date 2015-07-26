from thefuck import shells


def match(command, settings):
    return (command.script.startswith('tsuru')
            and 'not authenticated' in command.stderr
            and 'session has expired' in command.stderr)


def get_new_command(command, settings):
    return shells.and_('tsuru login', command.script)
