# Appends .py when compiling python files
# 
# Example:
# > python foo
# error: python: can't open file 'foo': [Errno 2] No such file or directory

#
# 

def match(command, settings):
	return (command.script.startswith ('python ')
			and not command.script.endswith('.py'))

def get_new_command(command, settings):
	return command.script + '.py'
