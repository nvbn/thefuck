def match(command):

    return (
        command.script == "init"
    )




def get_new_command(command):
    return (command.script.replace("init","git init",1))
