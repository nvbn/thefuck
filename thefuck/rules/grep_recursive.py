def match(command, settings):
	return (command.script.startswith('grep')
            and 'is a directory' in command.stderr.lower())


def get_new_command(command, settings):
    return 'grep -r {}'.format(command.script[5:])
