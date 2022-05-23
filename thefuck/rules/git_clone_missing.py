from thefuck.specific.git import git_support

# Note: could probably use better checking for URLs

@git_support
def match(command):
    return command.script.endswith('.git') and (
        (  # HTTP cloning
            command.script.startswith('https://')
            or command.script.startswith('http://')
        )
        or (  # SSH cloning: user@website.com:path/to/repo.git
            command.script.find('@') < command.script.find(':')
            and command.script.find('@') != -1
            and command.script.find(':') != -1
        )
    )


@git_support
def get_new_command(command):
    return 'git clone ' + command.script
