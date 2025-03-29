from thefuck.specific.git import git_support


@git_support
def match(command):
    return (' rm ' in command.script
            and "fatal: not removing '" in command.output
            and "' recursively without -r" in command.output)


@git_support
def get_new_command(command):
    command_parts = command.script_parts[:]
    index = command_parts.index('rm') + 1
    command_parts.insert(index, '-r')
    return u' '.join(command_parts)
