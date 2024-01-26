def match(command):

    return (
        command.script == "status"
    )




def get_new_command(command):
    return (command.script.replace("status","git status",1))