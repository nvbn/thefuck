def match(command):

    return (
        command.script == "commit"
    )




def get_new_command(command):
    return (command.script.replace("commit","git commit",1))
