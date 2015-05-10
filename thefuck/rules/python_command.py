from thefuck.utils import sudo_support
# add 'python' suffix to the command if
#  1) The script does not have execute permission or
#  2) is interpreted as shell script


@sudo_support
def match(command, settings):
    toks = command.script.split()
    return (len(toks) > 0
            and toks[0].endswith('.py')
            and ('Permission denied' in command.stderr or
                 'command not found' in command.stderr))


@sudo_support
def get_new_command(command, settings):
    return 'python ' + command.script
