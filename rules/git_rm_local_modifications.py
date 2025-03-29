from thefuck.specific.git import git_support


@git_support
def match(command):
    return (' rm ' in command.script and
            'error: the following file has local modifications' in command.output and
            'use --cached to keep the file, or -f to force removal' in command.output)


@git_support
def get_new_command(command):
    command_parts = command.script_parts[:]
    index = command_parts.index('rm') + 1
    command_parts.insert(index, '--cached')
    command_list = [u' '.join(command_parts)]
    command_parts[index] = '-f'
    command_list.append(u' '.join(command_parts))
    return command_list
