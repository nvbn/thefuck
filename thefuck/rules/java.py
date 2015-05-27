# Fixes common java command mistake
# 
# Example:
# > java foo.java
# Error: Could not find or load main class foo.java
# 

def match(command, settings):
	return (command.script.startswith ('java ')
		and command.script.endswith ('.java'))

def get_new_command(command, settings):
	return command.script[:-5]
