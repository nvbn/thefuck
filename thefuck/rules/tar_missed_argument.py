# The purpose of this rule is to add arguments to the command tar if the user
# forgets to type them or he / she does not know that they exist.

# This is a list with some possible arguments, which come after the command tar.
arguments = [
    "-cvf",
    "-cvfj",
    "-cvzf",
    "-jxvf",
    "-xvf",
    "-zxvf"
]


# This fucntion:

# checks if '-' exist in the command.script. If there is the rule will not work.
# But if it does not exist, this means that the user has forgot to type an argupent
# after the command tar.

# checks if the word 'tar' exists in the command.script, because the rule is working
# only for the command tar.

# checks if the typed command is invalid, in order to correct it.
def match(command):
    return ('-' not in command.script and 'tar' in command.script and
            ('invalid option' in command.output or 'try' in command.output or
             'Try' in command.output or 'tar' in command.output))


# This function returns some possible arguments that can be typed after the command tar.
def get_new_command(command):
    new_commands = []
    for arg in arguments:
        new_commands.append(
            command.script[:4] + arg + " " + command.script[4:])
    return new_commands
