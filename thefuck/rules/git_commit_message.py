from thefuck.specific.git import git_support

@git_support
def match(command):
    return "commit" in command.script_parts

@git_support
def get_new_command(command):
    command_parts = command.script_parts[:]
    index = command_parts.index('commit') + 1
    command_parts.insert(index, '-m')
    return ' '.join(command_parts)
