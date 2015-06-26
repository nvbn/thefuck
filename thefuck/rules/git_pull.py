from thefuck import shells


def match(command, settings):
    return ('git' in command.script
            and 'pull' in command.script
            and 'set-upstream' in command.stderr)


def get_new_command(command, settings):
    line = command.stderr.split('\n')[-3].strip()
    branch = line.split(' ')[-1]
    set_upstream = line.replace('<remote>', 'origin')\
                       .replace('<branch>', branch)
    return shells.and_(set_upstream, command.script)
