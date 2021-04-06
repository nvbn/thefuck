from thefuck.specific.git import git_support


@git_support
def match(command):
    return "'master'" in command.output.lower() or "'main'" in command.output.lower()


@git_support
def get_new_command(command):
    if "'master'" in command.output.lower():
        return command.script.replace("master", "main")
    else:
        return command.script.replace("main", "master")
