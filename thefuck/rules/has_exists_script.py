import os

def match(command, settings):
	exist = os.path.exists(command.script)
	return exist

def get_new_command(command, settings):
    return './{}'.format(command.script)

