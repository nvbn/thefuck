from thefuck.specific.git import git_support


@git_support
def match(command):
    return (' rm ' in command.script
            and "fatal: not removing '" in command.stderr
            and "' recursively without -r" in command.stderr)


@git_support
def get_new_command(command):
    index = command.script_parts.index('rm') + 1
    command.script_parts.insert(index, '-r')
    return u' '.join(command.script_parts)
