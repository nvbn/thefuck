import os
from thefuck.utils import for_app

@for_app('uninstall', at_least=1)
def match(command):
	return (
		command.output.startswith('uninstall: ')and
		'command not found' incommand output
	)
def get_new_command(command):
	return command.script.replace('uninstall','rm',1)
