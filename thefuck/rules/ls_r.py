# Replaces "ls -r" with "ls -R"
# Since -r is normally used for recursion,
# many users probably attempt to use it
# with ls. However, ls -r merely reverses
# the output of ls. The proper flag is -R.

def match(command):
    return command.script == 'ls -r'


def get_new_command(command):
    return 'ls -R'
