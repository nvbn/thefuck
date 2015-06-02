# Fixes careless " and ' usage
# 
# Example:
# > git commit -m 'My Message"
# 
#
# 

def match(command, settings):
    return ('\'' in command.script
            and '\"' in command.script)

def get_new_command(command, settings):
    return command.script.replace ('\'', '\"')
