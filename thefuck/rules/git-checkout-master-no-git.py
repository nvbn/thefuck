def match(command):

    return (
        command.script == "checkout master"
    )




def get_new_command(command):
    return (command.script.replace("checkout master","git checkout master",1))
