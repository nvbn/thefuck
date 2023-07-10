def match(command):
##
    return (
        command.script == "add ."
    )




def get_new_command(command):
    return (command.script.replace("add .","git add .",1))
