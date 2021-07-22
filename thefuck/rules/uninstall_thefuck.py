def match(command):
        return('uninstall' in command.script and 'thefuck' in command.script)

def get_new_command(command):
        new_commands = []
        new_commands.append('What thefuck are you doing? Are you sure you want to uninstall? [Arrow down to uninstall]')

        if('command not found' not in command.output):
                new_commands.append(command.script)

        return new_commands
