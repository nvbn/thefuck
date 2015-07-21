from thefuck import shells, utils


@utils.git_support
def match(command, settings):
    return ('pull' in command.script
            and 'set-upstream' in command.stderr)


@utils.git_support
def get_new_command(command, settings):
    line = command.stderr.split('\n')[-3].strip()
    branch = line.split(' ')[-1]
    set_upstream = line.replace('<remote>', 'origin')\
                       .replace('<branch>', branch)
    return shells.and_(set_upstream, command.script)
