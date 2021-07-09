from thefuck.specific.git import git_support


@git_support
def match(command):
    return "'master'" in command.output or "'main'" in command.output


@git_support
def get_new_command(command):
    if "'master'" in command.output:
        return command.script.replace("master", "main")
    return command.script.replace("main", "master")


priority = 1200
