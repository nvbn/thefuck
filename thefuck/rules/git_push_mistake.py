from thefuck.logs import debug
###
def match(command):
    debug('{}'.format(command.script))
    return (
        command.script == "git push origin/main"
    )




def get_new_command(command):
    return (command.script.replace("origin/main","origin main",1))