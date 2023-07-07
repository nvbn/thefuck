

def match(command):
    
    return (
        command.script == "git push origin/main"
    )




def get_new_command(command):
    return (command.script.replace("origin/main","origin main",1))