def match(command):
    return 'git commit ' in command.script and ('Untracked files' in command.output
            or '''use "git add"''' in command.output or 'Changes not staged for commit'
            in command.output)


def get_new_command(command):
    return 'git add --all && ' + command.script


priority = 900
