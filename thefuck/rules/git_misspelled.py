# The function git_support can not be useful if a command has the word "git" misspelled.
# The purpose of this rule is to unfuck the commands like: gti commit -m 'message'.
# Without this rule, for example, if you try to unfuck this command the result will be:
# git commit -m message. This means that the quotation marks do not return.

# This is a list with the most used and common git commands
git_commands = [
    'add',
    'archive',
    'bisect',
    'branch',
    'clone',
    'commit',
    'config',
    'diff',
    'fetch',
    'fsck',
    'gc',
    'grep',
    'init',
    'log',
    'merge',
    'mv',
    'prune',
    'pull',
    'push',
    'rebase',
    'remote',
    'reset',
    'restore',
    'rm',
    'show',
    'status',
    'switch',
    'tag',
]

# Checks if the command is not found.
# It also checks if there is a git command in the command.script, for example 'commit' or 'push',
# using the list "git_commands" from above.
# It does this, because in order to understand if the typing command has
# to do with a git command.
def match(command):
    return 'not found' in command.output and command.script_parts[1] in git_commands


# This function replaces the misspelled command 'git'.
# We checked before if the typing command has to do with git or not,
# because this function always returns git in the begining of the
# command.script.
# For example if we type: cx thefuck (instead of: cd thefuck) and
# then try to unfuck this command, we do not want to return: git thefuck.
# But if we type: gti commit -m "message", the function will return
# git commit -m "message", which is the command that we wanted to type from the begining
def get_new_command(command):
    return 'git' + str(command.script)[len(command.script_parts[0]):]


priority = 1300
